from aiogram.types import Message, CallbackQuery

from core import langs
from core.settings import dp, storage, EXAMPLES_ERROR_TEXT, EXAMPLES_ARE_DONE_TEXT
from core.database import db
from core.parser import get_message_text_by_parsing_examples
from core.translator import translate, detect
from utils.buttons import get_ikb
from utils.decorators import typing_action, check_user_existance
from utils.text import FormattedText


def get_message_template(text):
    return f"""
Результаты:

    {FormattedText('Русский').bold()} - {translate(text, dest='ru')}
    {FormattedText('English').bold()} - {translate(text, dest='en')}
    {FormattedText('Français').bold()} - {translate(text, dest='fr')}
    {FormattedText('Deutsch').bold()} - {translate(text, dest='de')}
    {FormattedText('Español').bold()} - {translate(text, dest='es')}
    {FormattedText('Italian').bold()} - {translate(text, dest='it')}
            """


# Handle when got a sentence
@dp.message_handler(lambda message: len(message.text.split()) > 1)
@typing_action
@check_user_existance
async def handle_empty_message(message: Message, *args, **kwargs):
    db.translated += 1
    return await message.answer(text=get_message_template(message.text))


# Handle when got a single word
@dp.message_handler(lambda message: len(message.text.split()) == 1)
@typing_action
@check_user_existance
async def handle_empty_message(message: Message, *args, **kwargs):
    db.translated += 1

    src = langs.BY_CODE.get(detect(message.text))
    await storage.update_data(user=message.from_user.id, data={"examples_number": 3, "src": src, "word": message.text})

    markup = get_ikb([{"text": lang, "callback_data": lang} for lang in langs.get_allowed(src)])
    await message.answer(text=get_message_template(message.text) + "Нажми на кнопку, чтобы получить примеры",
                         reply_markup=markup)


@dp.callback_query_handler(text=["more_examples", *langs.BY_NAME.keys()])
@typing_action
async def handle_get_examples(call: CallbackQuery, *args, **kwargs):
    if call.data != "more_examples":
        await storage.update_data(user=call.from_user.id, data={"dest": call.data})

    user_id = call.from_user.id
    data = await storage.get_data(user=user_id)

    # If script was restarted, storage is clear.
    # So there is no any data about source, destination language and word itself
    if "examples_number" not in data:
        return await call.answer("These buttons are too old")

    await storage.update_data(user=user_id, data={"examples_number": data["examples_number"] + 3})

    await call.answer("Loading...")
    text = await get_message_text_by_parsing_examples()

    message_text = "Все примеры показаны"
    markup = None
    if text != EXAMPLES_ARE_DONE_TEXT:
        message_text = text
        markup = get_ikb({"text": "Еще примеры", "callback_data": "more_examples"})
    elif text == EXAMPLES_ERROR_TEXT:
        message_text = text

    await call.message.answer(text=message_text, reply_markup=markup)
