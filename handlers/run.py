from aiogram import executor
from loader import dp


def run_bot():
    executor.start_polling(dp, skip_updates=True)
