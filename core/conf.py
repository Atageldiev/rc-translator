import importlib
import os

from dotenv import load_dotenv

load_dotenv()

settings = importlib.import_module(os.getenv("BOT_SETTINGS_MODULE"))
