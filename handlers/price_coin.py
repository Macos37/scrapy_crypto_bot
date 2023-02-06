from dispatcher import dp,bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup,State

from keyboards.keyboards import button_price
from models_api.requests_api import get_coin_top10,get_global_market,get_trending


class Form(StatesGroup):
    
    pass


@dp.message_handler(commands=['start'])
async def send_welcom(message: types.Message):
    await message.answer('Hi I\'am Robot',reply_markup=button_price)
    

@dp.callback_query_handler(text='get_price_top10')
async def send_price_top10(callback:types.CallbackQuery):
    info = ''
    coins = get_coin_top10()
    for coin_key in coins:
        percent = f'🔴' if coins[coin_key]['percent_change_24h'] < 0 else f'🟢'
        info+=f"Coin: <b>{coin_key}</b> 💎\n\
        - price: <b>{coins[coin_key]['price']}</b> 💰\n\
        - percent_change_24h: <b>{coins[coin_key]['percent_change_24h']:.2f}% {percent}</b>\n\
        - market_cap: <b>{coins[coin_key]['market_cap']}</b>\n\
        - volume_24h: <b>{coins[coin_key]['volume_24h']}</b>\n\n"
    await callback.message.edit_text(info,reply_markup=button_price)
    await callback.answer()
    
@dp.callback_query_handler(text='get_global_market')
async def send_global_market(callback: types.CallbackQuery):
    biggest_gainers,biggest_losers = await get_trending(True),await get_trending(False)
    market = await get_global_market()
    up = '🟢 Biggest Gainers\n'
    down = '🔴 Biggest Losers\n'
    for dict_coin in biggest_gainers,biggest_losers:
        if dict_coin is biggest_losers:
            for key,value in dict_coin.items():
                down+=f'<b>{key}</b> - {value[0]}  {value[1]:.2f}%\n'
        else:
            for key,value in dict_coin.items():
                up+=f'<b>{key}</b> - {value[0]}  {value[1]:.2f}%\n'          
    result = f'Market Cap: <b>{market[0]}</b> 💎\n\
Volume 24h: <b>{market[1]}</b> 💸\n\
Dominance: <b>{market[2]}</b>\n\
ETH Gas: <b>{market[3]} Gwei 🔥</b>\n\n{up}\n{down}'
    await callback.message.edit_text(result,reply_markup=button_price)
    await callback.answer()