# import from aiogram
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# import from other modules


# import from custom files
from config import TOKEN
from myclass import Sqlighter, Parser


# Initialize bot and dispatcher
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

# Initialize class object
db = Sqlighter()
Parser = Parser()