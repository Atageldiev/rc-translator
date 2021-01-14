from aiogram.dispatcher.filters import Command
from aiogram.types import (
    Message, CallbackQuery,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup, InlineKeyboardButton
)

from core.conf import dp, settings
from utils import LearningMode
from utils.database import db
from utils.decorators import typing_action, check_user_existance


@dp.message_handler(Command("setsub"))
@typing_action
@check_user_existance
async def setsub(message: Message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Subscribe/unsubscribe", callback_data="sub_unsub"))
    markup.add(InlineKeyboardButton(text="Change learning mode", callback_data="learning_mode"))

    await message.answer("Что вы хотите сделать?", reply_markup=markup)


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
    learning_mode = db.get_value("learning_mode")
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    learning_modes = settings.LEARNING_MODE

    for el in learning_modes.keys():
        markup.insert(f"Mode {el}")
    markup.add("Cancel")

    await call.message.reply(
        f"Доступные режимы обучения: \n\n1 - {learning_modes.get(1)}\n2 - {learning_modes.get(2)}\n\n<b>Внимание!</b>\nВремя в каждом режиме прописано по Бишкекскому\n(GMT+06)")
    await call.message.reply(
        f"Ваш активный режим обучения: <em>{learning_modes.get(learning_modes)}</em>\n\n<em><u>Нажмите на соответствующую кнопку, чтобы изменить режим</u></em>",
        reply_markup=markup)
    await LearningMode.mode.set()
