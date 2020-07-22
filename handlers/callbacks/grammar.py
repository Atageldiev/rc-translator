from aiogram.types import CallbackQuery, InlineKeyboardMarkup, \
    InlineKeyboardButton

from loader import dp, parser
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
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Определение частицы | Definition of the particles", url="https://www.native-english.ru/grammar/english-particles"))
    markup.add(InlineKeyboardButton(text="Различие частиц | Difference of the particles", url="https://www.native-english.ru/grammar/particles-differ"))
    await callback_query.message.answer("<b>Найденный материал по частицам: </b>", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == "parts")
async def parts(callback_query: CallbackQuery):
    await callback_query.answer("Loading...")
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Главные | Main", callback_data="main_parts"))
    markup.add(InlineKeyboardButton(text="Второстепенные | Secondary", callback_data="secondary_parts"))
    await callback_query.message.answer("<b>Найденный материал по членам предложения: </b>", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == "main_parts")
async def main_parts(callback_query: CallbackQuery):
    await callback_query.answer("Loading...")
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Подлежащее | Subject", url="https://www.native-english.ru/grammar/english-subject"))
    markup.add(InlineKeyboardButton(text="Сказуемое | Predicate", url="https://www.native-english.ru/grammar/english-predicate"))
    await callback_query.message.answer("<b>Найденный материал по главным членам предложения: </b>", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == "secondary_parts")
async def secondary_parts(callback_query: CallbackQuery):
    await callback_query.answer("Loading...")
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Дополнение | Object", url="https://www.native-english.ru/grammar/english-object"))
    markup.add(InlineKeyboardButton(text="Определение | Attribute", url="https://www.native-english.ru/grammar/english-attribute"))
    markup.add(InlineKeyboardButton(text="Обстоятельство | Adverbial", url="https://www.native-english.ru/grammar/english-adverbial"))
    markup.add(InlineKeyboardButton(text="Не члены предложения | Not parts of a sentence", url="https://www.native-english.ru/grammar/not-sentence"))
    await callback_query.message.answer("<b>Найденный материал по второстепенным членам предложения: </b>", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == "simple_sentences")
async def simple_sentences(callback_query: CallbackQuery):
    await callback_query.answer("Loading...")
    markup = InlineKeyboardMarkup()    
    markup.add(InlineKeyboardButton(text="Определение | Definition", url="https://www.native-english.ru/grammar/simple-sentences"))
    markup.add(InlineKeyboardButton(text="Порядок слов | Word order", url="https://www.native-english.ru/grammar/word-order"))
    markup.add(InlineKeyboardButton(text="Инверсия | Inversion", url="https://www.native-english.ru/grammar/inversion"))
    markup.add(InlineKeyboardButton(text="Общий вопрос | General question", url="https://www.native-english.ru/grammar/general-questions"))
    markup.add(InlineKeyboardButton(text="Специальный вопрос | Special questions", url="https://www.native-english.ru/grammar/special-questions"))
    markup.add(InlineKeyboardButton(text="Повелительное предложение | Imperative sentence", url="https://www.native-english.ru/grammar/imperative-sentences"))
    markup.add(InlineKeyboardButton(text="Восклицательное предложение | Exclamatory sentence", url="https://www.native-english.ru/grammar/exclamatory-sentences"))
    await callback_query.message.answer("<b>Найденный материал по простым предложениям: </b>", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == "complex_sentences")
async def complex_sentences(callback_query: CallbackQuery):
    await callback_query.answer("Loading...")
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Сложносочиненное | Compound", url="https://www.native-english.ru/grammar/compound-sentences"))
    markup.add(InlineKeyboardButton(text="Сложноподчиненное | Complex", url="https://www.native-english.ru/grammar/complex-sentences"))
    markup.add(InlineKeyboardButton(text="Условное | Conditional", url="https://www.native-english.ru/grammar/conditional-sentences"))
    await callback_query.message.answer("<b>Найденный материал по сложным предложениям: </b>", reply_markup=markup)    

@dp.callback_query_handler(lambda c: c.data == "indirect_speech")
async def indirect_speech(callback_query: CallbackQuery):
    await callback_query.answer("Loading...")
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Определение | Definition", url="https://www.native-english.ru/grammar/indirect-speech"))
    markup.add(InlineKeyboardButton(text="Согласование времен | Sequence of tenses", url="https://www.native-english.ru/grammar/sequence-of-tenses"))
    await callback_query.message.answer("<b>Найденный материал по косвенной речи: </b>", reply_markup=markup)    


