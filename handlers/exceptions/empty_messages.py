from aiogram.types import Message, CallbackQuery

from core.conf import dp, storage, LANGCODES, ALLOWED_LANGS
from utils.formatters import bold
from library.handlers.class_based import MessageHandler
from utils.buttons import get_ikb
from utils.database import db
from utils.decorators import check_user_existance, typing_action
from utils.other import get_key_by_value
from utils.parser import parse_examples
from utils.translator import translate, detect


class EmptyMessageHandler(MessageHandler):
    decorators = [typing_action, check_user_existance]

    async def handle(self, message: Message):
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


@dp.callback_query_handler(text=["more_examples", *[lang_key for lang_key in LANGCODES.values()]])
async def send_examples(call: CallbackQuery):
    user_id = call.from_user.id
    data = await storage.get_data(user=user_id)
    if call.data != "more_examples":
        dest = get_key_by_value(call.data, LANGCODES)
        await storage.update_data(user=user_id, data={"dest": dest})

    num = data["num"]
    await storage.update_data(user=user_id, data={"num": num + 3})
    data = await storage.get_data(user=user_id)

    await call.answer("Loading...")

    text, markup = parse_examples(data, data["num"])
    if text != "Вот примеры\n":
        await call.message.answer(text=text, reply_markup=markup)
    else:
        await call.message.edit_text(text="Все примеры показаны", reply_markup=None)
