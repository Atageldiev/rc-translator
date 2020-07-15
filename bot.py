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

# import from aiogram
from aiogram import executor
from aiogram.types import Message, CallbackQuery

# import from my files
from loader import dp, db, bot
from config import ADMIN_ID
from command_handler import *
from callback_handler import *
from utils import WordStates, AdminStates, LearnerStates
from mymodule import backUpDB_task

# Configure logging
logging = logging.basicConfig(level=logging.INFO)
db.create_table_status()

# Handle all commands
@dp.message_handler(commands="start")
async def procces_command_start(message: Message):
    await command_start(message)

@dp.message_handler(commands="translate") # Тут выберется язык для перевода
async def procces_command_translate(message: Message):
    await command_translate(message)

@dp.message_handler(commands="grammar")
async def process_command_grammar(message: Message):
    await command_grammar(message)

@dp.message_handler(commands="rating")
async def process_command_rating(message: Message):
    await command_rating(message)

@dp.message_handler(commands="setsub")
async def process_command_setsub(message: Message):
    await command_setsub(message)

@dp.message_handler(lambda message: message.from_user.id == ADMIN_ID, commands="users", commands_prefix="!")
async def process_command_users(message: Message):
    await admin_command_users(message)

@dp.message_handler(lambda message: message.from_user.id == ADMIN_ID, commands="send_all", commands_prefix="!")
async def process_command_send_all(message: Message):
    await admin_command_send_all(message)

@dp.message_handler(lambda message: message.from_user.id == ADMIN_ID, commands="send_one", commands_prefix="!")
async def process_command_send_one(message: Message):
    message = message.text.split("!send_one").pop(-1).split("/")
    await answer_by_chat_id(chat_id=message[0].strip(" "), text=f"My father @t2elzeth says: \n'<em>{message[1]}</em>'")

@dp.message_handler(lambda message: message.from_user.id == ADMIN_ID, commands="setDB", commands_prefix="!")
async def process_command_setDB(message: Message):
    await admin_command_setDB(message)

@dp.message_handler(lambda message: message.from_user.id != ADMIN_ID)
async def process_empty_messages(message: Message):
    from_user = message.from_user
    await answer_by_chat_id(chat_id=ADMIN_ID, text=f"<b>{from_user.first_name}</b> says:\n'<em>{message.text}</em>'\n\
user_id:{from_user.id}", disable_notification=True)


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


@dp.message_handler(state=AdminStates.all()[1])
async def process_admin_state_setDB(message: Message):
    await admin_state_setDB(message)

@dp.message_handler(state=LearnerStates.all()[0])
async def process_learnerState_0(message: Message):
    await learnerState_0(message)


# Handle all inline-buttons
@dp.callback_query_handler(lambda c: c.data == "sub_unsub")
async def process_sub_unsub(callback_query: CallbackQuery):
    await sub_unsub(callback_query)

@dp.callback_query_handler(lambda c: c.data == "sub")
async def process_sub(callback_query: CallbackQuery):
    await sub(callback_query)

@dp.callback_query_handler(lambda c: c.data == "unsub")
async def process_unsub(callback_query: CallbackQuery):
    await unsub(callback_query)

@dp.callback_query_handler(lambda c: c.data == "learning_mode")
async def process_learning_mode(callback_query: CallbackQuery):
    await learning_mode(callback_query)


@dp.callback_query_handler(lambda c: c.data == "show_examples")
async def process_show_examples(callback_query: CallbackQuery):
    await show_examples(callback_query)

@dp.callback_query_handler(lambda c: c.data == "articles")
async def process_articles(callback_query: CallbackQuery):
    await articles(callback_query)

@dp.callback_query_handler(lambda c: c.data == "verb")
async def process_verb(callback_query: CallbackQuery):
    await verb(callback_query)

@dp.callback_query_handler(lambda c: c.data == "noun")
async def process_noun(callback_query: CallbackQuery):
    await noun(callback_query)

@dp.callback_query_handler(lambda c: c.data == "adjective")
async def process_adjective(callback_query: CallbackQuery):
    await adjective(callback_query)

@dp.callback_query_handler(lambda c: c.data == "pronoun")
async def process_pronoun(callback_query: CallbackQuery):
    await pronoun(callback_query)

@dp.callback_query_handler(lambda c: c.data == "numeral")
async def process_numeral(callback_query: CallbackQuery):
    await numeral(callback_query)

@dp.callback_query_handler(lambda c: c.data == "adverb")
async def process_adverb(callback_query: CallbackQuery):
    await adverb(callback_query)

@dp.callback_query_handler(lambda c: c.data == "preposition")
async def process_preposition(callback_query: CallbackQuery):
    await preposition(callback_query)

@dp.callback_query_handler(lambda c: c.data == "conjunction")
async def process_conjunction(callback_query: CallbackQuery):
    await conjunction(callback_query)

@dp.callback_query_handler(lambda c: c.data == "particles")
async def process_particles(callback_query: CallbackQuery):
    await particles(callback_query)

@dp.callback_query_handler(lambda c: c.data == "parts")
async def process_parts(callback_query: CallbackQuery):
    await parts(callback_query)

@dp.callback_query_handler(lambda c: c.data == "main_parts")
async def process_main_parts(callback_query: CallbackQuery):
    await main_parts(callback_query)

@dp.callback_query_handler(lambda c: c.data == "secondary_parts")
async def process_secondary_parts(callback_query: CallbackQuery):
    await secondary_parts(callback_query)

@dp.callback_query_handler(lambda c: c.data == "simple_sentences")
async def process_simple_sentences(callback_query: CallbackQuery):
    await simple_sentences(callback_query)

@dp.callback_query_handler(lambda c: c.data == "complex_sentences")
async def process_complex_sentences(callback_query: CallbackQuery):
    await complex_sentences(callback_query)

@dp.callback_query_handler(lambda c: c.data == "indirect_speech")
async def process_indirect_speech(callback_query: CallbackQuery):
    await indirect_speech(callback_query)

if __name__ == '__main__':
    dp.loop.create_task(backUpDB_task())
    executor.start_polling(dp, skip_updates=True)
    
