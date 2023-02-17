from dispatcher import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from db.request_db import register_user, add_coin, get_user_token, check_coin

from keyboards.keyboards import button_price, ReplyKeyboardRemove
from models_api.requests_api import get_coin_top10, get_global_market, get_trending


class Form(StatesGroup):
    
    pass


@dp.message_handler(commands=['start'])
async def send_welcom(message: types.Message):
    reg = await register_user(user_id=message.from_user.id, first_name=message.from_user.first_name)
    await message.answer(f'Hi I\'am Robot\n{reg}', reply_markup=button_price)


@dp.callback_query_handler(text='get_price_top10')
async def send_price_top10(callback: types.CallbackQuery):
    info = ''
    coins = get_coin_top10()
    for key, value in coins.items():
        percent = '🔴' if value.percent_change_24h < 0 else '🟢'
        info += f"Coin: <b>{key}</b> 💎\n\
        - price: <b>{value.price}</b> 💰\n\
        - percent_change_24h: <b>{value.percent_change_24h}% {percent}</b>\n\
        - market_cap: <b>{value.market_cap}</b>\n\
        - volume_24h: <b>{value.volume_24h}</b>\n\n"
    await callback.message.edit_text(info, reply_markup=button_price)
    
    
@dp.callback_query_handler(text='get_global_market')
async def send_global_market(callback: types.CallbackQuery):
    biggest_gainers, biggest_losers = await get_trending(True), await get_trending(False)
    market = await get_global_market()
    up = '🟢 Biggest Gainers\n'
    down = '🔴 Biggest Losers\n'
    for dict_coin in biggest_gainers, biggest_losers:
        if dict_coin is biggest_losers:
            for key, value in dict_coin.items():
                down += f'<b>{key}</b> - {value[0]}  {value[1]:.2f}%\n'
        else:
            for key, value in dict_coin.items():
                up += f'<b>{key}</b> - {value[0]}  {value[1]:.2f}%\n'          
    result = f'Market Cap: <b>{market[0]}</b> 💎\n\
Volume 24h: <b>{market[1]}</b> 💸\n\
Dominance: <b>{market[2]}</b>\n\
ETH Gas: <b>{market[3]} Gwei 🔥</b>\n\n{up}\n{down}'
    await callback.message.edit_text(result, reply_markup=button_price)


@dp.callback_query_handler(text='add_token')
async def add_token(callback: types.CallbackQuery):
    await callback.message.answer('How add token you want? text please.\
Example <b>\'BTC\'</b> or <b>BTC,ETH</b>', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(content_types=['text'])
async def token(message: types.Message):
    if ',' in message.text:
        coins = message.text.split(',')
        for coin in coins:
            add = await add_coin(coin, message.from_user.id)
    else:
        coin = message.text
        add = await add_coin(coin, message.from_user.id)
        
    await message.answer(add)

   
@dp.callback_query_handler(text='get_token')
async def get_token(callback: types.CallbackQuery):
    res = await get_user_token(callback.from_user.id)
    await callback.message.edit_text(res, reply_markup=button_price)
