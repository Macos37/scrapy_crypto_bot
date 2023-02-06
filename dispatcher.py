from aiogram import Bot,Dispatcher,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv,find_dotenv
import os



storage_memory = MemoryStorage()
load_dotenv(find_dotenv())
bot = Bot(token=os.getenv('TOKEN'),parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot,storage=storage_memory)