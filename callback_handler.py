# import from aiogram
from aiogram import types

# import from my files
from loader import db, Parser, dp
from config import STATUS, LEARNING_MODE
from utils import LearnerStates

async def show_examples(callback_query):
    user_id = callback_query.from_user.id

    word = db.get_value(name="word", user_id=user_id)
    lang_from = db.get_value(name="lang_from", user_id=user_id)
    lang_into = db.get_value(name="lang_into", user_id=user_id)
    num = db.get_value(name="num", user_id=user_id)

    await callback_query.answer("Loading...")
    await Parser.parse(callback_query.message, word, lang_from, lang_into, state=2, num=num)
    
    db.update_value(name="num", value=num+3, user_id=user_id)
    
async def sub_unsub(callback_query):
    status = db.get_value(name="subbed", user_id=callback_query.from_user.id)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Subscribe", callback_data="sub"))
    markup.add(types.InlineKeyboardButton(text="Unsubscribe", callback_data="unsub"))
    await callback_query.message.edit_text(f"Ваш активный статус: <em>{STATUS.get(status)}</em>", reply_markup=markup)

async def sub(callback_query):
    db.update_value(name="subbed", value=True, user_id=callback_query.from_user.id)

    status = "Subscribed"

    await callback_query.answer("Success!")
    await callback_query.message.edit_text(f"Ваш активный статус: <em>{status}</em>", reply_markup=None)

async def unsub(callback_query):
    db.update_value(name="subbed", value=False, user_id=callback_query.from_user.id)

    status = "Unsubscribed"

    await callback_query.answer("Success!")
    await callback_query.message.edit_text(f"Ваш активный статус: <em>{status}</em>", reply_markup=None)


async def learning_mode(callback_query):
    user_id = callback_query.from_user.id
    state = dp.current_state(user=user_id)
    learning_mode = db.get_value("learning_mode", user_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    for el in LEARNING_MODE.keys():
        markup.insert(types.KeyboardButton(f"Mode {el}"))
    markup.add(types.KeyboardButton("Cancel"))

    await callback_query.message.reply(f"Доступные режимы обучения: \n\n1 - {LEARNING_MODE.get(1)}\n2 - {LEARNING_MODE.get(2)}\n3 - {LEARNING_MODE.get(3)}\n\n<b>Внимание!</b>\nВремя в каждом режиме прописано по МСК")
    await callback_query.message.reply(f"Ваш активный режим обучения: <em>{LEARNING_MODE.get(learning_mode)}</em>\n\n<em><u>Нажмите на соответствующую кнопку, чтобы изменить режим</u></em>", reply_markup=markup)
    await state.set_state(LearnerStates.all()[0])

async def articles(callback_query):
    await callback_query.answer("Loading...")
    await Parser.parse_native_english(callback_query.message, "https://www.native-english.ru/grammar/english-articles")

async def verb(callback_query):
    await callback_query.answer("Loading...")
    await Parser.parse_native_english(
        callback_query.message, "https://www.native-english.ru/grammar/english-verbs")
    
async def noun(callback_query):
    await callback_query.answer("Loading...")
    await Parser.parse_native_english(callback_query.message, "https://www.native-english.ru/grammar/english-nouns")

async def adjective(callback_query):
    await callback_query.answer("Loading...")
    await Parser.parse_native_english(callback_query.message, "https://www.native-english.ru/grammar/english-adjectives")

async def pronoun(callback_query):
    await callback_query.answer("Loading...")
    await Parser.parse_native_english(callback_query.message, "https://www.native-english.ru/grammar/english-pronouns")

async def numeral(callback_query):
    await callback_query.answer("Loading...")
    await Parser.parse_native_english(callback_query.message, "https://www.native-english.ru/grammar/english-numerals")

async def adverb(callback_query):
    await callback_query.answer("Loading...")
    await Parser.parse_native_english(callback_query.message, "https://www.native-english.ru/grammar/english-adverbs")

async def preposition(callback_query):
    await callback_query.answer("Loading...")
    await Parser.parse_native_english(callback_query.message, "https://www.native-english.ru/grammar/english-prepositions")

async def conjunction(callback_query):
    await callback_query.answer("Loading...")
    await Parser.parse_native_english(callback_query.message, "https://www.native-english.ru/grammar/english-conjunctions")

async def particles(callback_query):
    await callback_query.answer("Loading...")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Определение частицы | Definition of the particles", url="https://www.native-english.ru/grammar/english-particles"))
    markup.add(types.InlineKeyboardButton(text="Различие частиц | Difference of the particles", url="https://www.native-english.ru/grammar/particles-differ"))
    await callback_query.message.answer("<b>Найденный материал по частицам: </b>", reply_markup=markup)

async def parts(callback_query):
    await callback_query.answer("Loading...")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Главные | Main", callback_data="main_parts"))
    markup.add(types.InlineKeyboardButton(text="Второстепенные | Secondary", callback_data="secondary_parts"))
    await callback_query.message.answer("<b>Найденный материал по членам предложения: </b>", reply_markup=markup)

async def main_parts(callback_query):
    await callback_query.answer("Loading...")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Подлежащее | Subject", url="https://www.native-english.ru/grammar/english-subject"))
    markup.add(types.InlineKeyboardButton(text="Сказуемое | Predicate", url="https://www.native-english.ru/grammar/english-predicate"))
    await callback_query.message.answer("<b>Найденный материал по главным членам предложения: </b>", reply_markup=markup)

async def secondary_parts(callback_query):
    await callback_query.answer("Loading...")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Дополнение | Object", url="https://www.native-english.ru/grammar/english-object"))
    markup.add(types.InlineKeyboardButton(text="Определение | Attribute", url="https://www.native-english.ru/grammar/english-attribute"))
    markup.add(types.InlineKeyboardButton(text="Обстоятельство | Adverbial", url="https://www.native-english.ru/grammar/english-adverbial"))
    markup.add(types.InlineKeyboardButton(text="Не члены предложения | Not parts of a sentence", url="https://www.native-english.ru/grammar/not-sentence"))
    await callback_query.message.answer("<b>Найденный материал по второстепенным членам предложения: </b>", reply_markup=markup)

async def simple_sentences(callback_query):
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

async def complex_sentences(callback_query):
    await callback_query.answer("Loading...")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Сложносочиненное | Compound", url="https://www.native-english.ru/grammar/compound-sentences"))
    markup.add(types.InlineKeyboardButton(text="Сложноподчиненное | Complex", url="https://www.native-english.ru/grammar/complex-sentences"))
    markup.add(types.InlineKeyboardButton(text="Условное | Conditional", url="https://www.native-english.ru/grammar/conditional-sentences"))
    await callback_query.message.answer("<b>Найденный материал по сложным предложениям: </b>", reply_markup=markup)    

async def indirect_speech(callback_query):
    await callback_query.answer("Loading...")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Определение | Definition", url="https://www.native-english.ru/grammar/indirect-speech"))
    markup.add(types.InlineKeyboardButton(text="Согласование времен | Sequence of tenses", url="https://www.native-english.ru/grammar/sequence-of-tenses"))
    await callback_query.message.answer("<b>Найденный материал по косвенной речи: </b>", reply_markup=markup)    


