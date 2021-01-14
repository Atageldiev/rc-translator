import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from googletrans import Translator

from data.config import TOKEN
from classes import Database, Parser, LearnerAPI

logging.basicConfig(level=logging.INFO,
                    format='ID-%(process)d:%(asctime)s:%(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

# Class instances
db = Database()
parser = Parser()
translator = Translator()
learner = LearnerAPI()
