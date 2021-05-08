import importlib

from aiogram import executor

from core.settings import dp

importlib.import_module("handlers")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
