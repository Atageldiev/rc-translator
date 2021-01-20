from aiogram import executor
from core.conf.settings import dp


def run_bot():
    executor.start_polling(dp, skip_updates=True)
