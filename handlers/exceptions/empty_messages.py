from aiogram.types import (
    Message, ChatActions,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton as IKB
)

from core.conf import dp, settings
from utils.database import db
from utils.decorators import check_user_existance
from utils.parser import parse_examples
from utils.translator import get_translation, get_src


@dp.message_handler()
@check_user_existance
async def sentence(message: Message):
    db.update_value("words_translated")
    text = message.text

    if len(text.split()) == 1:
        src = get_src(text)
        src = settings.LANGS.get(src)
        data = {
            "num": 3,
            "src": src,
            "word": text
        }
        await dp.storage.update_data(user=message.from_user.id, data=data)
        markup = InlineKeyboardMarkup(row_width=2)
        for el in settings.ALLOWED_LANGS.get(src):
            markup.insert(IKB(text=el, callback_data=settings.LANGCODES.get(el)))
    else:
        markup = InlineKeyboardMarkup()
        markup.add(IKB(text="Кнопок нет", callback_data="None"))

    await ChatActions.typing()
    res_ru = get_translation(text=text, dest="ru")
    res_en = get_translation(text=text, dest="en")
    res_fr = get_translation(text=text, dest="fr")
    res_de = get_translation(text=text, dest="de")
    res_es = get_translation(text=text, dest="es")

    await ChatActions.typing()
    await message.answer(
        text=f"Результаты: \n\
        <b> Русский </b> - {res_ru}\n\
        <b> English </b> - {res_en}\n\
        <b> Français </b> - {res_fr}\n\
        <b> Deutsch </b> - {res_de}\n\
        <b> Español </b > - {res_es}\n\nНажми на кнопку, чтобы получить примеры",
        reply_markup=markup
    )


@dp.callback_query_handler(text="more_examples")
@dp.callback_query_handler(text="ru")
@dp.callback_query_handler(text="en")
@dp.callback_query_handler(text="fr")
@dp.callback_query_handler(text="de")
@dp.callback_query_handler(text="es")
@dp.callback_query_handler(text="ja")
@dp.callback_query_handler(text="ar")
@dp.callback_query_handler(text="it")
@dp.callback_query_handler(text="tr")
@dp.callback_query_handler(text="zh-cn")
async def send_examples(call: CallbackQuery):
    user_id = call.from_user.id
    data = await dp.storage.get_data(user=user_id)

    if call.data != "more_examples":
        dest = settings.LANGS.get(call.data)
        await dp.storage.update_data(user=user_id, data={"dest": dest})

    num = data["num"]
    await dp.storage.update_data(user=user_id, data={"num": num + 3})
    data = await dp.storage.get_data(user=user_id)

    await call.answer("Loading...")

    text, markup = parse_examples(data, data["num"])
    if text != "Вот примеры\n":
        await call.message.answer(text=text, reply_markup=markup)
    else:
        await call.message.edit_text(text="Все примеры показаны", reply_markup=None)


@dp.callback_query_handler(text="None")
async def none_call_data(call: CallbackQuery):
    await call.answer(text="При переводе предложений кнопки не поддерживаются", show_alert=True)
