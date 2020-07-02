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
from loader import dp, db
from config import ADMIN_ID
from command_handler import *
from callback_handler import *
from utils import WordStates, AdminStates

# Configure logging
logging = logging.basicConfig(level=logging.INFO)
db.create_table()

# Handle all commands
@dp.message_handler(commands="start")
async def procces_command_start(message: Message):
    await command_start(message)

@dp.message_handler(commands="translate") # Тут выберется язык для перевода
async def procces_command_translate(message: Message):
    await command_translate(message)

@dp.message_handler(lambda message: message.from_user.id == ADMIN_ID, commands="users", commands_prefix="!")
async def process_command_users(message: Message):
    await admin_command_users(message)

@dp.message_handler(lambda message: message.from_user.id == ADMIN_ID, commands="send_all", commands_prefix="!")
async def process_command_send_all(message: Message):
    await admin_command_send_all(message)

# Handle all states
@dp.message_handler(state=WordStates.all()[0])
async def process_state_choose_lang_into(message: Message):
    await state_choose_lang_into(message)


@dp.message_handler(state=WordStates.all()[1])
async def process_state_choose_lang_into(message: Message):
    await state_send_word(message)

@dp.message_handler(state=WordStates.all()[2])
async def process_state_send_word(message: Message):
    await state_send_result(message)

@dp.message_handler(state=AdminStates.all()[0])
async def process_state_send_message_all(message: Message):
    await admin_state_send_message_all(message)


# Handle all inline-buttons
@dp.callback_query_handler(lambda c: c.data == "show_examples")
async def process_show_examples(callback_query: CallbackQuery):
    await show_examples(callback_query)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    
