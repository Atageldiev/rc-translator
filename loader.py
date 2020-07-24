#---------------------------------------------------------------------------
#   imports
#---------------------------------------------------------------------------
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from googletrans import Translator

from data.config import TOKEN
from classes import DB_API, Parser, LEARNER_API

# Some configuration
# filename = "data/bot.log",
logging.basicConfig(level=logging.INFO,
                    format='ID-%(process)d:%(asctime)s:%(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
#---------------------------------------------------------------------------
#   Initialize required objects
#---------------------------------------------------------------------------
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

# Class objects
db = DB_API()
parser = Parser()
translator = Translator()
learner = LEARNER_API()