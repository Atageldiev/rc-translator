"""
Файл bot.py - каркасс из разных функций, собранных их разных модулей


Все функции для обработки команд в файле command_handler.py
Все функции для обработки callback'ов в файле callback_handler.py
Все функции по работе с БД прописаны в классе Sqlighter в файле myclass.py
Все дополнительные/вспомогательные функции в файле mymodule.py

Все классы в файле myclass.py

Все нужные константы в config.py

Инициализация необходимых переменных в loader
"""
# import required libraries
import logging
import schedule

# import from aiogram
from aiogram import executor
from aiogram.types import Message, CallbackQuery

# import from my files
from loader import dp
from command_handler import send_welcome, command_translate, translate_state_0
from utils import States

# Configure logging
logging = logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands="start")
async def procces_send_welcome(message: Message):
    await send_welcome(message)

@dp.message_handler(commands="translate")
async def procces_translate(message: Message):
    await command_translate(message)


@dp.message_handler(state=States.STATE_0)
async def process_translate_state_0(message: Message):
    await translate_state_0(message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    
