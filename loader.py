# import from aiogram
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# import from custom files
from data.config import TOKEN
from classes.myclass import Sqlighter, Parser


# Initialize bot and dispatcher
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

# Initialize class objects
db = Sqlighter()
Parser = Parser()