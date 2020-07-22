import logging 

from aiogram.types import CallbackQuery, InlineKeyboardMarkup, \
    InlineKeyboardButton, ReplyKeyboardMarkup

from loader import dp, db
from data.config import LEARNING_MODE
from utils import LearningMode

@dp.callback_query_handler(lambda c: c.data == "sub_unsub")
async def sub_unsub(callback_query: CallbackQuery):
    if db.get_value(name="subbed"):
        status = "Subscribed"
    else:
        status = "Unsubscribed"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Subscribe", callback_data="sub"))
    markup.add(InlineKeyboardButton(text="Unsubscribe", callback_data="unsub"))
    await callback_query.message.edit_text(f"Ваш активный статус: <em>{status}</em>", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == "sub")
async def sub(callback_query: CallbackQuery):
    db.update_value(name="subbed", value=True)

    status = "Subscribed"

    await callback_query.answer("Success!")
    await callback_query.message.edit_text(f"Ваш активный статус: <em>{status}</em>", reply_markup=None)

@dp.callback_query_handler(lambda c: c.data == "unsub")
async def unsub(callback_query: CallbackQuery):
    db.update_value(name="subbed", value=False)

    status = "Unsubscribed"

    await callback_query.answer("Success!")
    await callback_query.message.edit_text(f"Ваш активный статус: <em>{status}</em>", reply_markup=None)

@dp.callback_query_handler(lambda c: c.data == "learning_mode")
async def learning_mode(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id

    learning_mode = db.get_value("learning_mode")
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    for el in LEARNING_MODE.keys():
        markup.insert(f"Mode {el}")
    markup.add("Cancel")

    await callback_query.message.reply(f"Доступные режимы обучения: \n\n1 - {LEARNING_MODE.get(1)}\n2 - {LEARNING_MODE.get(2)}\n3 - {LEARNING_MODE.get(3)}\n\n<b>Внимание!</b>\nВремя в каждом режиме прописано по МСК")
    await callback_query.message.reply(f"Ваш активный режим обучения: <em>{LEARNING_MODE.get(learning_mode)}</em>\n\n<em><u>Нажмите на соответствующую кнопку, чтобы изменить режим</u></em>", reply_markup=markup)
    await LearningMode.mode.set()
