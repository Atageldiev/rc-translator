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

logging.basicConfig(filename="mylog.log",level=logging.INFO,                                # Configure logging
                    format='ID-%(process)d:%(asctime)s:%(levelname)s:%(message)s', datefmt='%d-%b-%y %H:%M:%S')

from aiogram import executor
from aiogram.types import Message, CallbackQuery

# import from my files
from handlers.commands import command, admin
from handlers.callbacks import callback

from loader import dp, db
from data.config import ADMIN_ID

from utils.utils import WordStates, AdminStates, LearnerStates

db.create_table_status()

logging.info("Bot has been successfully started!")

# Handle all commands
@dp.message_handler(commands="start")
async def procces_command_start(message: Message):
    await command.command_start(message)

@dp.message_handler(commands="translate")
async def procces_command_translate(message: Message):
    await command.command_translate(message)

@dp.message_handler(commands="grammar")
async def process_command_grammar(message: Message):
    await command.command_grammar(message)

@dp.message_handler(commands="rating")
async def process_command_rating(message: Message):
    await command.command_rating(message)

@dp.message_handler(commands="setsub")
async def process_command_setsub(message: Message):
    await command.command_setsub(message)

@dp.message_handler(lambda message: message.from_user.id == ADMIN_ID, commands="users", commands_prefix="!")
async def process_command_users(message: Message):
    await admin.command_users(message)
    

@dp.message_handler(lambda message: message.from_user.id == ADMIN_ID, commands="send_all", commands_prefix="!")
async def process_command_send_all(message: Message):
    await admin.command_send_all(message)

@dp.message_handler(lambda message: message.from_user.id == ADMIN_ID, commands="send_one", commands_prefix="!")
async def process_command_send_one(message: Message):
    await admin.command_send_one(message)

@dp.message_handler(lambda message: message.from_user.id == ADMIN_ID, commands="setDB", commands_prefix="!")
async def process_command_setDB(message: Message):
    await admin.command_setDB(message)

@dp.message_handler(lambda message: message.from_user.id == ADMIN_ID, commands="send_log", commands_prefix="!")
async def process_command_send_log(message: Message):
    await admin.command_send_log(message)

@dp.message_handler(lambda message: message.from_user.id != ADMIN_ID)
async def process_empty_messages(message: Message):
    await admin.empty_messages(message)


# Handle all states
@dp.message_handler(state=WordStates.all()[0])
async def process_state_choose_lang_into(message: Message):
    await command.state_choose_lang_into(message)

@dp.message_handler(state=WordStates.all()[1])
async def process_state_choose_lang_into(message: Message):
    await command.state_send_word(message)

@dp.message_handler(state=WordStates.all()[2])
async def process_state_send_word(message: Message):
    await command.state_send_result(message)

@dp.message_handler(state=AdminStates.all()[0])
async def process_state_send_message_all(message: Message):
    await admin.state_send_message_all(message)

@dp.message_handler(state=AdminStates.all()[1])
async def process_state_setDB(message: Message):
    await admin.state_setDB(message)

@dp.message_handler(state=LearnerStates.all()[0])
async def process_learnerState_0(message: Message):
    await command.state_learningMode0(message)


# Handle all inline-buttons
@dp.callback_query_handler(lambda c: c.data == "sub_unsub")
async def process_sub_unsub(callback_query: CallbackQuery):
    await callback.sub_unsub(callback_query)

@dp.callback_query_handler(lambda c: c.data == "sub")
async def process_sub(callback_query: CallbackQuery):
    await callback.sub(callback_query)

@dp.callback_query_handler(lambda c: c.data == "unsub")
async def process_unsub(callback_query: CallbackQuery):
    await callback.unsub(callback_query)

@dp.callback_query_handler(lambda c: c.data == "learning_mode")
async def process_learning_mode(callback_query: CallbackQuery):
    await callback.learning_mode(callback_query)


@dp.callback_query_handler(lambda c: c.data == "show_examples")
async def process_show_examples(callback_query: CallbackQuery):
    await callback.show_examples(callback_query)

@dp.callback_query_handler(lambda c: c.data == "articles")
async def process_articles(callback_query: CallbackQuery):
    await callback.articles(callback_query)

@dp.callback_query_handler(lambda c: c.data == "verb")
async def process_verb(callback_query: CallbackQuery):
    await callback.verb(callback_query)

@dp.callback_query_handler(lambda c: c.data == "noun")
async def process_noun(callback_query: CallbackQuery):
    await callback.noun(callback_query)

@dp.callback_query_handler(lambda c: c.data == "adjective")
async def process_adjective(callback_query: CallbackQuery):
    await callback.adjective(callback_query)

@dp.callback_query_handler(lambda c: c.data == "pronoun")
async def process_pronoun(callback_query: CallbackQuery):
    await callback.pronoun(callback_query)

@dp.callback_query_handler(lambda c: c.data == "numeral")
async def process_numeral(callback_query: CallbackQuery):
    await callback.numeral(callback_query)

@dp.callback_query_handler(lambda c: c.data == "adverb")
async def process_adverb(callback_query: CallbackQuery):
    await callback.adverb(callback_query)

@dp.callback_query_handler(lambda c: c.data == "preposition")
async def process_preposition(callback_query: CallbackQuery):
    await callback.preposition(callback_query)

@dp.callback_query_handler(lambda c: c.data == "conjunction")
async def process_conjunction(callback_query: CallbackQuery):
    await callback.conjunction(callback_query)

@dp.callback_query_handler(lambda c: c.data == "particles")
async def process_particles(callback_query: CallbackQuery):
    await callback.particles(callback_query)

@dp.callback_query_handler(lambda c: c.data == "parts")
async def process_parts(callback_query: CallbackQuery):
    await callback.parts(callback_query)

@dp.callback_query_handler(lambda c: c.data == "main_parts")
async def process_main_parts(callback_query: CallbackQuery):
    await callback.main_parts(callback_query)

@dp.callback_query_handler(lambda c: c.data == "secondary_parts")
async def process_secondary_parts(callback_query: CallbackQuery):
    await callback.secondary_parts(callback_query)

@dp.callback_query_handler(lambda c: c.data == "simple_sentences")
async def process_simple_sentences(callback_query: CallbackQuery):
    await callback.simple_sentences(callback_query)

@dp.callback_query_handler(lambda c: c.data == "complex_sentences")
async def process_complex_sentences(callback_query: CallbackQuery):
    await callback.complex_sentences(callback_query)

@dp.callback_query_handler(lambda c: c.data == "indirect_speech")
async def process_indirect_speech(callback_query: CallbackQuery):
    await callback.indirect_speech(callback_query)
    

if __name__ == '__main__':

    from modules.mymodule import setTask

    dp.loop.create_task(setTask())
    executor.start_polling(dp, skip_updates=True)
    
