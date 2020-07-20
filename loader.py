#---------------------------------------------------------------------------
#   imports
#---------------------------------------------------------------------------
import logging

# filename = "data/bot.log",
logging.basicConfig(level=logging.INFO,
                    format='ID-%(process)d:%(asctime)s:%(levelname)s - [%(filename)s:%(lineno)d] - %(message)s', 
                    datefmt='%d-%b-%y %H:%M:%S')

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from googletrans import Translator

from data.config import TOKEN
from classes.myclass import Database, Parser


#---------------------------------------------------------------------------
#   Initialize required objects
#---------------------------------------------------------------------------
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

# Class objects
db = Database()
Parser = Parser()
translator = Translator()

# on_startup
db.create_table_status()
