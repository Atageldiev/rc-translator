import os
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from classes import Database, Parser, LearnerAPI
from data.config import TOKEN

BASE_DIR = Path(__file__).resolve().parent

logging.basicConfig(level=logging.INFO,
                    filename=os.path.join(BASE_DIR, ".log"),
                    format='ID-%(process)d:%(asctime)s:%(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

# Class instances
db = Database()
parser = Parser()
learner = LearnerAPI()
