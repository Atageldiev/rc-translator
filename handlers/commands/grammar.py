from aiogram.types import (
    Message, ChatActions,
    CallbackQuery, InlineKeyboardMarkup,
    InlineKeyboardButton
    )
from aiogram.dispatcher.filters import Command

from loader import dp, db, parser

@dp.message_handler(Command("grammar"))
async def grammar(message: Message):
    db.user_id_exists()
    grammar_used = db.get_value(name="grammar_used")
    db.update_value(name="grammar_used", value=grammar_used + 1)

    markup = InlineKeyboardMarkup(row_width=3)
    markup.insert(InlineKeyboardButton(
        text="Глагол | Verb", callback_data="verb"))
    markup.insert(InlineKeyboardButton(
        text="Артикли | Articles", callback_data="articles"))
    markup.insert(InlineKeyboardButton(
        text="Существительное | Noun", callback_data="noun"))
    markup.insert(InlineKeyboardButton(
        text="Прилагательное | Adjective", callback_data="adjective"))
    markup.insert(InlineKeyboardButton(
        text="Местоимение | Pronoun", callback_data="pronoun"))
    markup.insert(InlineKeyboardButton(
        text="Числительное | Numeral", callback_data="numeral"))
    markup.insert(InlineKeyboardButton(
        text="Наречие | Adverb", callback_data="adverb"))
    markup.insert(InlineKeyboardButton(
        text="Предлог | Preposition", callback_data="preposition"))
    markup.insert(InlineKeyboardButton(
        text="Союз | Conjunction", callback_data="conjunction"))
    markup.insert(InlineKeyboardButton(
        text="Частица | Particles", callback_data="particles"))
    markup.insert(InlineKeyboardButton(text="Междометие | Interjections",
                                    url="https://www.native-english.ru/grammar/english-interjections"))
    markup.insert(InlineKeyboardButton(
        text="Члены предложения | Parts of a sentence", callback_data="parts"))
    markup.insert(InlineKeyboardButton(
        text="Простые предложения | Simple sentences", callback_data="simple_sentences"))
    markup.insert(InlineKeyboardButton(
        text="Сложные предложения | Complex sentences", callback_data="complex_sentences"))
    markup.insert(InlineKeyboardButton(
        text="Косвенная речь | Indirect speech", callback_data="indirect_speech"))
    markup.insert(InlineKeyboardButton(text="Пунктуация | Punctuation",
                                    url="https://www.native-english.ru/grammar/english-punctuation"))

    await ChatActions.typing()
    await message.answer("Выберите насчет чего вы хотите получить готовую информацию: ", reply_markup=markup)


#---------------------------------------------------------------------------
#   Functions to handle inline-buttons that are created by /grammar command
#---------------------------------------------------------------------------
@dp.callback_query_handler(text="articles")
async def articles(call: CallbackQuery):
    await call.answer("Loading...")
    await parser.parse_native_english(call.message, "https://www.native-english.ru/grammar/english-articles")


@dp.callback_query_handler(text="verb")
async def verb(call: CallbackQuery):
    await call.answer("Loading...")
    await parser.parse_native_english(
        call.message, "https://www.native-english.ru/grammar/english-verbs")


@dp.callback_query_handler(text="noun")
async def noun(call: CallbackQuery):
    await call.answer("Loading...")
    await parser.parse_native_english(call.message, "https://www.native-english.ru/grammar/english-nouns")


@dp.callback_query_handler(text="adjective")
async def adjective(call: CallbackQuery):
    await call.answer("Loading...")
    await parser.parse_native_english(call.message, "https://www.native-english.ru/grammar/english-adjectives")


@dp.callback_query_handler(text="pronoun")
async def pronoun(call: CallbackQuery):
    await call.answer("Loading...")
    await parser.parse_native_english(call.message, "https://www.native-english.ru/grammar/english-pronouns")


@dp.callback_query_handler(text="numeral")
async def numeral(call: CallbackQuery):
    await call.answer("Loading...")
    await parser.parse_native_english(call.message, "https://www.native-english.ru/grammar/english-numerals")


@dp.callback_query_handler(text="adverb")
async def adverb(call: CallbackQuery):
    await call.answer("Loading...")
    await parser.parse_native_english(call.message, "https://www.native-english.ru/grammar/english-adverbs")


@dp.callback_query_handler(text="preposition")
async def preposition(call: CallbackQuery):
    await call.answer("Loading...")
    await parser.parse_native_english(call.message, "https://www.native-english.ru/grammar/english-prepositions")


@dp.callback_query_handler(text="conjunction")
async def conjunction(call: CallbackQuery):
    await call.answer("Loading...")
    await parser.parse_native_english(call.message, "https://www.native-english.ru/grammar/english-conjunctions")


@dp.callback_query_handler(text="particles")
async def particles(call: CallbackQuery):
    await call.answer("Loading...")
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Определение частицы | Definition of the particles",
                                    url="https://www.native-english.ru/grammar/english-particles"))
    markup.add(InlineKeyboardButton(text="Различие частиц | Difference of the particles",
                                    url="https://www.native-english.ru/grammar/particles-differ"))
    await call.message.answer("<b>Найденный материал по частицам: </b>", reply_markup=markup)


@dp.callback_query_handler(text="parts")
async def parts(call: CallbackQuery):
    await call.answer("Loading...")
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        text="Главные | Main", callback_data="main_parts"))
    markup.add(InlineKeyboardButton(
        text="Второстепенные | Secondary", callback_data="secondary_parts"))
    await call.message.answer("<b>Найденный материал по членам предложения: </b>", reply_markup=markup)


@dp.callback_query_handler(text="main_parts")
async def main_parts(call: CallbackQuery):
    await call.answer("Loading...")
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Подлежащее | Subject",
                                    url="https://www.native-english.ru/grammar/english-subject"))
    markup.add(InlineKeyboardButton(text="Сказуемое | Predicate",
                                    url="https://www.native-english.ru/grammar/english-predicate"))
    await call.message.answer("<b>Найденный материал по главным членам предложения: </b>", reply_markup=markup)


@dp.callback_query_handler(text="secondary_parts")
async def secondary_parts(call: CallbackQuery):
    await call.answer("Loading...")
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Дополнение | Object",
                                    url="https://www.native-english.ru/grammar/english-object"))
    markup.add(InlineKeyboardButton(text="Определение | Attribute",
                                    url="https://www.native-english.ru/grammar/english-attribute"))
    markup.add(InlineKeyboardButton(text="Обстоятельство | Adverbial",
                                    url="https://www.native-english.ru/grammar/english-adverbial"))
    markup.add(InlineKeyboardButton(text="Не члены предложения | Not parts of a sentence",
                                    url="https://www.native-english.ru/grammar/not-sentence"))
    await call.message.answer("<b>Найденный материал по второстепенным членам предложения: </b>", reply_markup=markup)


@dp.callback_query_handler(text="simple_sentences")
async def simple_sentences(call: CallbackQuery):
    await call.answer("Loading...")
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Определение | Definition",
                                    url="https://www.native-english.ru/grammar/simple-sentences"))
    markup.add(InlineKeyboardButton(text="Порядок слов | Word order",
                                    url="https://www.native-english.ru/grammar/word-order"))
    markup.add(InlineKeyboardButton(text="Инверсия | Inversion",
                                    url="https://www.native-english.ru/grammar/inversion"))
    markup.add(InlineKeyboardButton(text="Общий вопрос | General question",
                                    url="https://www.native-english.ru/grammar/general-questions"))
    markup.add(InlineKeyboardButton(text="Специальный вопрос | Special questions",
                                    url="https://www.native-english.ru/grammar/special-questions"))
    markup.add(InlineKeyboardButton(text="Повелительное предложение | Imperative sentence",
                                    url="https://www.native-english.ru/grammar/imperative-sentences"))
    markup.add(InlineKeyboardButton(text="Восклицательное предложение | Exclamatory sentence",
                                    url="https://www.native-english.ru/grammar/exclamatory-sentences"))
    await call.message.answer("<b>Найденный материал по простым предложениям: </b>", reply_markup=markup)


@dp.callback_query_handler(text="complex_sentences")
async def complex_sentences(call: CallbackQuery):
    await call.answer("Loading...")
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Сложносочиненное | Compound",
                                    url="https://www.native-english.ru/grammar/compound-sentences"))
    markup.add(InlineKeyboardButton(text="Сложноподчиненное | Complex",
                                    url="https://www.native-english.ru/grammar/complex-sentences"))
    markup.add(InlineKeyboardButton(text="Условное | Conditional",
                                    url="https://www.native-english.ru/grammar/conditional-sentences"))
    await call.message.answer("<b>Найденный материал по сложным предложениям: </b>", reply_markup=markup)


@dp.callback_query_handler(text="indirect_speech")
async def indirect_speech(call: CallbackQuery):
    await call.answer("Loading...")
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Определение | Definition",
                                    url="https://www.native-english.ru/grammar/indirect-speech"))
    markup.add(InlineKeyboardButton(text="Согласование времен | Sequence of tenses",
               url="https://www.native-english.ru/grammar/sequence-of-tenses"))
    await call.message.answer("<b>Найденный материал по косвенной речи: </b>", reply_markup=markup)
