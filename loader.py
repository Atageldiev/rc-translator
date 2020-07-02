# import from aiogram
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# import from custom files
# from myclass import Sqlighter
from config import TOKEN
from myclass import Sqlighter

# Initialize bot and dispatcher
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

# Initialize database object
db = Sqlighter()