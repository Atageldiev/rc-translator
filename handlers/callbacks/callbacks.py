#---------------------------------------------------------------------------
#   imports
#---------------------------------------------------------------------------
import logging
from aiogram import types
from aiogram.types import CallbackQuery

from loader import db, parser, dp
from data.config import LEARNING_MODE
from utils import LearningMode


#---------------------------------------------------------------------------
#   Functions
#---------------------------------------------------------------------------
@dp.callback_query_handler(lambda c: c.data == "show_examples")
async def show_examples(callback_query: CallbackQuery):
    """
    Sends 4 more examples, if available
    If not, converts text of the message that button is pinned to into "All of the examples have already been shown"
    """
    user_id = callback_query.from_user.id
    data = await dp.storage.get_data(user=user_id)

    num = data["num"]

    await callback_query.answer("Loading...")
    await parser.parse_examples(data, callback_query.message, num)
    
    await dp.storage.update_data(user=callback_query.from_user.id, data={"num": num + 3})
    

@dp.callback_query_handler(lambda c: c.data == "sub_unsub")
async def sub_unsub(callback_query: CallbackQuery):
    if db.get_value(name="subbed", user_id=callback_query.from_user.id):
        status = "Subscribed"
    else:
        status = "Unsubscribed"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Subscribe", callback_data="sub"))
    markup.add(types.InlineKeyboardButton(text="Unsubscribe", callback_data="unsub"))
    await callback_query.message.edit_text(f"Ваш активный статус: <em>{status}</em>", reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == "sub")
async def sub(callback_query: CallbackQuery):
    db.update_value(name="subbed", value=True, user_id=callback_query.from_user.id)

    status = "Subscribed"

    await callback_query.answer("Success!")
    await callback_query.message.edit_text(f"Ваш активный статус: <em>{status}</em>", reply_markup=None)

@dp.callback_query_handler(lambda c: c.data == "unsub")
async def unsub(callback_query: CallbackQuery):
    db.update_value(name="subbed", value=False, user_id=callback_query.from_user.id)

    status = "Unsubscribed"

    await callback_query.answer("Success!")
    await callback_query.message.edit_text(f"Ваш активный статус: <em>{status}</em>", reply_markup=None)

@dp.callback_query_handler(lambda c: c.data == "learning_mode")
async def learning_mode(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id

    learning_mode = db.get_value("learning_mode", user_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    for el in LEARNING_MODE.keys():
        markup.insert(types.KeyboardButton(f"Mode {el}"))
    markup.add(types.KeyboardButton("Cancel"))

    await callback_query.message.reply(f"Доступные режимы обучения: \n\n1 - {LEARNING_MODE.get(1)}\n2 - {LEARNING_MODE.get(2)}\n3 - {LEARNING_MODE.get(3)}\n\n<b>Внимание!</b>\nВремя в каждом режиме прописано по МСК")
    await callback_query.message.reply(f"Ваш активный режим обучения: <em>{LEARNING_MODE.get(learning_mode)}</em>\n\n<em><u>Нажмите на соответствующую кнопку, чтобы изменить режим</u></em>", reply_markup=markup)
    await LearningMode.mode.set()


#---------------------------------------------------------------------------
#   Functions to handle inline-buttons that are created by /grammar command
#---------------------------------------------------------------------------
@dp.callback_query_handler(lambda c: c.data == "articles")
async def articles(callback_query: CallbackQuery):
    await callback_query.answer("Loading...")
    await parser.parse_native_english(callback_query.message, "https://www.native-english.ru/grammar/english-articles")

@dp.callback_query_handler(lambda c: c.data == "verb")
async def verb(callback_query: CallbackQuery):
    await callback_query.answer("Loading...")
    await parser.parse_native_english(
        callback_query.message, "https://www.native-english.ru/grammar/english-verbs")
    
@dp.callback_query_handler(lambda c: c.data == "noun")
async def noun(callback_query: CallbackQuery):
    await callback_query.answer("Loading...")
    await parser.parse_native_english(callback_query.message, "https://www.native-english.ru/grammar/english-nouns")

@dp.callback_query_handler(lambda c: c.data == "adjective")
async def adjective(callback_query: CallbackQuery):
    await callback_query.answer("Loading...")
    await parser.parse_native_english(callback_query.message, "https://www.native-english.ru/grammar/english-adjectives")

@dp.callback_query_handler(lambda c: c.data == "pronoun")
async def pronoun(callback_query: CallbackQuery):
    await callback_query.answer("Loading...")
    await parser.parse_native_english(callback_query.message, "https://www.native-english.ru/grammar/english-pronouns")

@dp.callback_query_handler(lambda c: c.data == "numeral")
async def numeral(callback_query: CallbackQuery):
    await callback_query.answer("Loading...")
    await parser.parse_native_english(callback_query.message, "https://www.native-english.ru/grammar/english-numerals")

@dp.callback_query_handler(lambda c: c.data == "adverb")
async def adverb(callback_query: CallbackQuery):
    await callback_query.answer("Loading...")
    await parser.parse_native_english(callback_query.message, "https://www.native-english.ru/grammar/english-adverbs")

@dp.callback_query_handler(lambda c: c.data == "preposition")
async def preposition(callback_query: CallbackQuery):
    await callback_query.answer("Loading...")
    await parser.parse_native_english(callback_query.message, "https://www.native-english.ru/grammar/english-prepositions")


@dp.callback_query_handler(lambda c: c.data == "conjunction")
async def conjunction(callback_query: CallbackQuery):
    await callback_query.answer("Loading...")
    await parser.parse_native_english(callback_query.message, "https://www.native-english.ru/grammar/english-conjunctions")

@dp.callback_query_handler(lambda c: c.data == "particles")
async def particles(callback_query: CallbackQuery):
    await callback_query.answer("Loading...")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Определение частицы | Definition of the particles", url="https://www.native-english.ru/grammar/english-particles"))
    markup.add(types.InlineKeyboardButton(text="Различие частиц | Difference of the particles", url="https://www.native-english.ru/grammar/particles-differ"))
    await callback_query.message.answer("<b>Найденный материал по частицам: </b>", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == "parts")
async def parts(callback_query: CallbackQuery):
    await callback_query.answer("Loading...")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Главные | Main", callback_data="main_parts"))
    markup.add(types.InlineKeyboardButton(text="Второстепенные | Secondary", callback_data="secondary_parts"))
    await callback_query.message.answer("<b>Найденный материал по членам предложения: </b>", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == "main_parts")
async def main_parts(callback_query: CallbackQuery):
    await callback_query.answer("Loading...")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Подлежащее | Subject", url="https://www.native-english.ru/grammar/english-subject"))
    markup.add(types.InlineKeyboardButton(text="Сказуемое | Predicate", url="https://www.native-english.ru/grammar/english-predicate"))
    await callback_query.message.answer("<b>Найденный материал по главным членам предложения: </b>", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == "secondary_parts")
async def secondary_parts(callback_query: CallbackQuery):
    await callback_query.answer("Loading...")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Дополнение | Object", url="https://www.native-english.ru/grammar/english-object"))
    markup.add(types.InlineKeyboardButton(text="Определение | Attribute", url="https://www.native-english.ru/grammar/english-attribute"))
    markup.add(types.InlineKeyboardButton(text="Обстоятельство | Adverbial", url="https://www.native-english.ru/grammar/english-adverbial"))
    markup.add(types.InlineKeyboardButton(text="Не члены предложения | Not parts of a sentence", url="https://www.native-english.ru/grammar/not-sentence"))
    await callback_query.message.answer("<b>Найденный материал по второстепенным членам предложения: </b>", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == "simple_sentences")
async def simple_sentences(callback_query: CallbackQuery):
    await callback_query.answer("Loading...")
    markup = types.InlineKeyboardMarkup()    
    markup.add(types.InlineKeyboardButton(text="Определение | Definition", url="https://www.native-english.ru/grammar/simple-sentences"))
    markup.add(types.InlineKeyboardButton(text="Порядок слов | Word order", url="https://www.native-english.ru/grammar/word-order"))
    markup.add(types.InlineKeyboardButton(text="Инверсия | Inversion", url="https://www.native-english.ru/grammar/inversion"))
    markup.add(types.InlineKeyboardButton(text="Общий вопрос | General question", url="https://www.native-english.ru/grammar/general-questions"))
    markup.add(types.InlineKeyboardButton(text="Специальный вопрос | Special questions", url="https://www.native-english.ru/grammar/special-questions"))
    markup.add(types.InlineKeyboardButton(text="Повелительное предложение | Imperative sentence", url="https://www.native-english.ru/grammar/imperative-sentences"))
    markup.add(types.InlineKeyboardButton(text="Восклицательное предложение | Exclamatory sentence", url="https://www.native-english.ru/grammar/exclamatory-sentences"))
    await callback_query.message.answer("<b>Найденный материал по простым предложениям: </b>", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == "complex_sentences")
async def complex_sentences(callback_query: CallbackQuery):
    await callback_query.answer("Loading...")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Сложносочиненное | Compound", url="https://www.native-english.ru/grammar/compound-sentences"))
    markup.add(types.InlineKeyboardButton(text="Сложноподчиненное | Complex", url="https://www.native-english.ru/grammar/complex-sentences"))
    markup.add(types.InlineKeyboardButton(text="Условное | Conditional", url="https://www.native-english.ru/grammar/conditional-sentences"))
    await callback_query.message.answer("<b>Найденный материал по сложным предложениям: </b>", reply_markup=markup)    

@dp.callback_query_handler(lambda c: c.data == "indirect_speech")
async def indirect_speech(callback_query: CallbackQuery):
    await callback_query.answer("Loading...")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Определение | Definition", url="https://www.native-english.ru/grammar/indirect-speech"))
    markup.add(types.InlineKeyboardButton(text="Согласование времен | Sequence of tenses", url="https://www.native-english.ru/grammar/sequence-of-tenses"))
    await callback_query.message.answer("<b>Найденный материал по косвенной речи: </b>", reply_markup=markup)    


