from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

price_coin = InlineKeyboardButton('Get top 10 coins',callback_data='get_price_top10')
global_market = InlineKeyboardButton('Get global market',callback_data='get_global_market')
button_price =InlineKeyboardMarkup()
button_price.add(price_coin,global_market)
