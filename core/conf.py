import importlib
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

settings = importlib.import_module(os.getenv("BOT_SETTINGS_MODULE"))

bot = Bot(token=getattr(settings, "TOKEN"), parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())
