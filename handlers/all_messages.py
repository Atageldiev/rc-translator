from aiogram.types import Message, CallbackQuery

from core.conf import Langs
from core.conf.settings import dp, storage, EXAMPLES_ERROR_TEXT, EXAMPLES_ARE_DONE_TEXT
from core.database import db
from core.parser import get_message_text_by_parsing_examples
from core.translator import translate, detect
from utils.buttons import get_ikb
from utils.decorators import typing_action, check_user_existance
from utils.formatters import bold


def get_message_template(text):
    return f"Результаты: \n" \
           f"     {bold('Русский')} - {translate(text, dest='ru')}\n" \
           f"     {bold('English')} - {translate(text, dest='en')}\n" \
           f"     {bold('Français')} - {translate(text, dest='fr')}\n" \
           f"     {bold('Deutsch')} - {translate(text, dest='de')}\n" \
           f"     {bold('Español')} - {translate(text, dest='es')}\n" \
           f"     {bold('Italian')} - {translate(text, dest='it')}\n\n"


# Handle when got a sentence
@dp.message_handler(lambda message: len(message.text.split()) > 1)
@typing_action
@check_user_existance
async def handle_empty_message(message: Message):
    db.translated += 1
    return await message.answer(text=get_message_template(message.text))


# Handle when got a single word
@dp.message_handler(lambda message: len(message.text.split()) == 1)
@typing_action
@check_user_existance
async def handle_empty_message(message: Message):
    db.translated += 1

    src = Langs.BY_CODE.get(detect(message.text))
    await storage.update_data(user=message.from_user.id, data={"examples_number": 3, "src": src, "word": message.text})

    markup = get_ikb([{"text": lang, "callback_data": lang} for lang in Langs.get_allowed(src)])
    await message.answer(text=get_message_template(message.text) + "Нажми на кнопку, чтобы получить примеры",
                         reply_markup=markup)


@dp.callback_query_handler(text=[lang_key for lang_key in Langs.BY_NAME.keys()])
async def handle_get_examples(call: CallbackQuery):
    await storage.update_data(user=call.from_user.id, data={"dest": call.data})
    await send_examples(call)


@dp.callback_query_handler(text=["more_examples"])
async def handle_get_more_examples(call: CallbackQuery):
    await send_examples(call)


async def send_examples(call: CallbackQuery):
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
