import os
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

DEBUG = True
if DEBUG:
    TOKEN = "1397404758:AAEBfHXgaxWM0j-FGnsFsUxQjo4sMuyEz5Q"
else:
    TOKEN = "1368801526:AAFoG3C84uthcDinURZ031e2WOt9fcUzTjM"

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())
storage = dp.storage

# Admins chat_ids
ADMINS = [
    399344900
]

# Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(os.path.join(BASE_DIR, ".env.dev"))
# Database
DATABASE = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "db_name": os.getenv("DB_DB")
}

EXAMPLES_ARE_DONE_TEXT = "Вот примеры\n"
EXAMPLES_ERROR_TEXT = "ERROR, TRY AGAIN"
