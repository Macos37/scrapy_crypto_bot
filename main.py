from aiogram import executor
from dispatcher import dp
from handlers import price_coin
import logging


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp,skip_updates=True)