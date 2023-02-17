from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardRemove

price_coin = InlineKeyboardButton('Get top 10 coins',callback_data='get_price_top10')
global_market = InlineKeyboardButton('Get global market',callback_data='get_global_market')
add_token = InlineKeyboardButton('ADD BTC',callback_data='add_token')

get_token = InlineKeyboardButton('Get Token',callback_data='get_token')

button_price =InlineKeyboardMarkup(row_width=3)
button_price.add(price_coin,global_market,add_token,get_token)
