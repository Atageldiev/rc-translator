#---------------------------------------------------------------------------
#   imports
#---------------------------------------------------------------------------
import logging

from aiogram import types
from aiogram.types import Message, ChatActions, ChatType

from loader import dp, db
from data.config import LANGS
from utils import WordStates, SentenceStates

#---------------------------------------------------------------------------
#   Handlers
#---------------------------------------------------------------------------
@dp.message_handler(commands="start")
async def start(message: Message):
    
    db.user_id_exists(user_id=message.from_user.id, name=message.from_user.first_name)

    await ChatActions.typing()
    await message.reply("Привет, это бот для поиска переводов для различных слов\n/word\n/sentence")

@dp.message_handler(commands="grammar")
async def grammar(message: Message):
    db.user_id_exists(user_id=message.from_user.id, name=message.from_user.first_name)
    grammar_used = db.get_value(name="grammar_used", user_id=message.from_user.id)
    db.update_value(name="grammar_used", value=grammar_used + 1, user_id=message.from_user.id)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Глагол | Verb", callback_data="verb"))
    markup.add(types.InlineKeyboardButton(text="Артикли | Articles", callback_data="articles"))
    markup.add(types.InlineKeyboardButton(text="Существительное | Noun", callback_data="noun"))
    markup.add(types.InlineKeyboardButton(text="Прилагательное | Adjective", callback_data="adjective"))
    markup.add(types.InlineKeyboardButton(text="Местоимение | Pronoun", callback_data="pronoun"))
    markup.add(types.InlineKeyboardButton(text="Числительное | Numeral", callback_data="numeral"))
    markup.add(types.InlineKeyboardButton(text="Наречие | Adverb", callback_data="adverb"))
    markup.add(types.InlineKeyboardButton(text="Предлог | Preposition", callback_data="preposition"))
    markup.add(types.InlineKeyboardButton(text="Союз | Conjunction", callback_data="conjunction"))
    markup.add(types.InlineKeyboardButton(text="Частица | Particles", callback_data="particles"))
    markup.add(types.InlineKeyboardButton(text="Междометие | Interjections",url="https://www.native-english.ru/grammar/english-interjections"))
    markup.add(types.InlineKeyboardButton(text="Члены предложения | Parts of a sentence", callback_data="parts"))
    markup.add(types.InlineKeyboardButton(text="Простые предложения | Simple sentences", callback_data="simple_sentences"))
    markup.add(types.InlineKeyboardButton(text="Сложные предложения | Complex sentences", callback_data="complex_sentences"))
    markup.add(types.InlineKeyboardButton(text="Косвенная речь | Indirect speech", callback_data="indirect_speech"))
    markup.add(types.InlineKeyboardButton(text="Пунктуация | Punctuation", url="https://www.native-english.ru/grammar/english-punctuation"))

    await ChatActions.typing()
    await message.answer("Выберите насчет чего вы хотите получить готовую информацию: ", reply_markup=markup)

@dp.message_handler(commands="rating")
async def rating(message: Message):
    user_id = message.from_user.id
    name = message.from_user.first_name

    db.user_id_exists(user_id=user_id, name=name)

    words_translated = db.get_value(name="words_translated", user_id=user_id)
    grammar_used = db.get_value(name="grammar_used", user_id=user_id)

    await ChatActions.typing()
    await message.answer(f"<b><u>{name}</u></b>, ваша статистика:\n\
    <em>Слов переведено:</em>- {words_translated}\n \
    <em>Помощника по грамматике использовано:</em>- {grammar_used}\n")

@dp.message_handler(commands="setsub")
async def setsub(message: Message):
    db.user_id_exists(user_id=message.from_user.id, name=message.from_user.first_name)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Subscribe/unsubscribe", callback_data="sub_unsub"))
    markup.add(types.InlineKeyboardButton(text="Change learning mode", callback_data="learning_mode"))

    await ChatActions.typing()
    await message.answer("Что вы хотите сделать?", reply_markup=markup)

@dp.message_handler(commands="word")
async def translate(message: Message):
    await dp.storage.update_data(user=message.from_user.id, data={"num": 3})
    db.user_id_exists(user_id=message.from_user.id, name=message.from_user.first_name)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True)
    for element in LANGS:
        markup.insert(element)

    await ChatActions.typing()
    await WordStates.dest.set()
    await message.answer("Выберите язык <b><u>с которого</u></b> хотите перевести", reply_markup=markup)

@dp.message_handler(commands="sentence")
async def sentence(message: Message):
    db.user_id_exists(user_id=message.from_user.id, name=message.from_user.first_name)
    markup = types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard =True, resize_keyboard =True)
    for el in LANGS:
        markup.insert(el)

    await ChatActions.typing()
    await message.answer("Выберите язык <b><u>с которого</u></b> хотите перевести", reply_markup=markup)
    await SentenceStates.dest.set()
