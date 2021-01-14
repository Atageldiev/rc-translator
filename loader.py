from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from classes import Database, Parser, LearnerAPI
from core.conf import settings

BASE_DIR = Path(__file__).resolve().parent

bot = Bot(token=settings.TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

# Class instances
db = Database()
parser = Parser()
learner = LearnerAPI()
