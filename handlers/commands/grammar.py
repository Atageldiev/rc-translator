from aiogram.types import Message, ChatActions, \
    InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, db

@dp.message_handler(commands="grammar")
async def grammar(message: Message):
    db.user_id_exists()
    grammar_used = db.get_value(name="grammar_used")
    db.update_value(name="grammar_used", value=grammar_used + 1)

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        text="Глагол | Verb", callback_data="verb"))
    markup.add(InlineKeyboardButton(
        text="Артикли | Articles", callback_data="articles"))
    markup.add(InlineKeyboardButton(
        text="Существительное | Noun", callback_data="noun"))
    markup.add(InlineKeyboardButton(
        text="Прилагательное | Adjective", callback_data="adjective"))
    markup.add(InlineKeyboardButton(
        text="Местоимение | Pronoun", callback_data="pronoun"))
    markup.add(InlineKeyboardButton(
        text="Числительное | Numeral", callback_data="numeral"))
    markup.add(InlineKeyboardButton(
        text="Наречие | Adverb", callback_data="adverb"))
    markup.add(InlineKeyboardButton(
        text="Предлог | Preposition", callback_data="preposition"))
    markup.add(InlineKeyboardButton(
        text="Союз | Conjunction", callback_data="conjunction"))
    markup.add(InlineKeyboardButton(
        text="Частица | Particles", callback_data="particles"))
    markup.add(InlineKeyboardButton(text="Междометие | Interjections",
                                    url="https://www.native-english.ru/grammar/english-interjections"))
    markup.add(InlineKeyboardButton(
        text="Члены предложения | Parts of a sentence", callback_data="parts"))
    markup.add(InlineKeyboardButton(
        text="Простые предложения | Simple sentences", callback_data="simple_sentences"))
    markup.add(InlineKeyboardButton(
        text="Сложные предложения | Complex sentences", callback_data="complex_sentences"))
    markup.add(InlineKeyboardButton(
        text="Косвенная речь | Indirect speech", callback_data="indirect_speech"))
    markup.add(InlineKeyboardButton(text="Пунктуация | Punctuation",
                                    url="https://www.native-english.ru/grammar/english-punctuation"))

    await ChatActions.typing()
    await message.answer("Выберите насчет чего вы хотите получить готовую информацию: ", reply_markup=markup)
