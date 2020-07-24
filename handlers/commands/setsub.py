import logging

from aiogram.types import (
    Message, CallbackQuery,
    ReplyKeyboardMarkup, ChatActions,
    InlineKeyboardMarkup, InlineKeyboardButton
    )
from aiogram.dispatcher.filters import Command

from loader import dp, db
from data.config import LEARNING_MODE
from utils import LearningMode

@dp.message_handler(Command("setsub"))
async def setsub(message: Message):
    db.user_id_exists()

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        text="Subscribe/unsubscribe", callback_data="sub_unsub"))
    markup.add(InlineKeyboardButton(
        text="Change learning mode", callback_data="learning_mode"))

    await ChatActions.typing()
    await message.answer("Что вы хотите сделать?", reply_markup=markup)

#---------------------------------------------------------------------------
#   Functions to handle inline-buttons that are created by /setsub command
#---------------------------------------------------------------------------
@dp.callback_query_handler(text="sub_unsub")
async def sub_unsub(call: CallbackQuery):
    if db.get_value(name="subbed"):
        status = "Subscribed"
    else:
        status = "Unsubscribed"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Subscribe", callback_data="sub"))
    markup.add(InlineKeyboardButton(text="Unsubscribe", callback_data="unsub"))
    await call.message.edit_text(f"Ваш активный статус: <em>{status}</em>", reply_markup=markup)

@dp.callback_query_handler(text="sub")
async def sub(call: CallbackQuery):
    db.update_value(name="subbed", value=True)

    status = "Subscribed"

    await call.answer("Success!")
    await call.message.edit_text(f"Ваш активный статус: <em>{status}</em>", reply_markup=None)

@dp.callback_query_handler(text="unsub")
async def unsub(call: CallbackQuery):
    db.update_value(name="subbed", value=False)

    status = "Unsubscribed"

    await call.answer("Success!")
    await call.message.edit_text(f"Ваш активный статус: <em>{status}</em>", reply_markup=None)


@dp.callback_query_handler(text="learning_mode")
async def learning_mode(call: CallbackQuery):
    user_id = call.from_user.id

    learning_mode = db.get_value("learning_mode")
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    for el in LEARNING_MODE.keys():
        markup.insert(f"Mode {el}")
    markup.add("Cancel")

    await call.message.reply(f"Доступные режимы обучения: \n\n1 - {LEARNING_MODE.get(1)}\n2 - {LEARNING_MODE.get(2)}\n\n<b>Внимание!</b>\nВремя в каждом режиме прописано по Бишкекскому\n(GMT+06)")
    await call.message.reply(f"Ваш активный режим обучения: <em>{LEARNING_MODE.get(learning_mode)}</em>\n\n<em><u>Нажмите на соответствующую кнопку, чтобы изменить режим</u></em>", reply_markup=markup)
    await LearningMode.mode.set()
