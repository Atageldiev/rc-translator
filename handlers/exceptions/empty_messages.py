from aiogram.types import Message, CallbackQuery

from core.conf.settings import dp, storage, LANGCODES, ALLOWED_LANGS
from core.database import db
from core.parser import get_message_text_by_parsing_examples
from core.translator import translate, detect
from utils.buttons import get_ikb
from utils.formatters import bold
from utils.other import get_key_by_value


@dp.message_handler()
async def handle_empty_message(message: Message):
    db.translated += 1
    text = message.text

    message_template = f"Результаты: \n" \
                       f"     {bold('Русский')} - {translate(text, dest='ru')}\n" \
                       f"     {bold('English')} - {translate(text, dest='en')}\n" \
                       f"     {bold('Français')} - {translate(text, dest='fr')}\n" \
                       f"     {bold('Deutsch')} - {translate(text, dest='de')}\n" \
                       f"     {bold('Español')} - {translate(text, dest='es')}\n\n"

    # If got a sentence
    if len(text.split()) > 1:
        return await message.answer(text=message_template)

    src = get_key_by_value(detect(text), LANGCODES)
    await storage.update_data(user=message.from_user.id, data={"num": 3, "src": src, "word": text})

    button_data = [{"text": el, "callback_data": LANGCODES.get(el)} for el in ALLOWED_LANGS.get(src)]
    await message.answer(text=message_template + "Нажми на кнопку, чтобы получить примеры",
                         reply_markup=get_ikb(button_data))


@dp.callback_query_handler(text=[lang_key for lang_key in LANGCODES.values()])
async def handle_get_examples(c: CallbackQuery):
    user_id = c.from_user.id
    await storage.update_data(user=user_id, data={"dest": get_key_by_value(c.data, LANGCODES)})

    await send_examples(c)


@dp.callback_query_handler(text=["more_examples"])
async def handle_get_more_examples(call: CallbackQuery):
    await send_examples(call)


async def send_examples(call: CallbackQuery):
    user_id = call.from_user.id
    data = await storage.get_data(user=user_id)
    await storage.update_data(user=user_id, data={"num": data["num"] + 3})
    data = await storage.get_data(user=user_id)

    await call.answer("Loading...")
    text = get_message_text_by_parsing_examples(data, data["num"])
    if text != "Вот примеры\n":
        await call.message.answer(text=text,
                                  reply_markup=get_ikb({"text": "Еще примеры", "callback_data": "more_examples"}))
    else:
        await call.message.answer(text="Все примеры показаны", reply_markup=None)
