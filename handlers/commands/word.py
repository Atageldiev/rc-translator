import logging

from aiogram.types import (
    Message, CallbackQuery,
    ChatActions, ReplyKeyboardMarkup
    )
from aiogram.dispatcher.filters import Command

from loader import dp, db, parser
from data.config import LANGS
from utils import Word

@dp.message_handler(Command("word"))
async def translate(message: Message):
    await dp.storage.update_data(user=message.from_user.id, data={"num": 3})

    db.user_id_exists()

    markup = ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=3, one_time_keyboard=True)

    for element in LANGS:
        markup.insert(element)

    await ChatActions.typing()
    await Word.dest.set()
    await message.answer("Выберите язык <b><u>с которого</u></b> хотите перевести", reply_markup=markup)


#---------------------------------------------------------------------------
#   Functions to handle inline-buttons that are created by /word command
#---------------------------------------------------------------------------
@dp.callback_query_handler(lambda c: c.data == "show_examples")
async def show_examples(call: CallbackQuery):
    """
    Sends 4 more examples, if available
    If not, converts text of the message that button is pinned to into "All of the examples have already been shown"
    """
    user_id = call.from_user.id
    data = await dp.storage.get_data(user=user_id)

    num = data["num"]

    await call.answer("Loading...")
    await parser.parse_examples(data, call.message, num)

    await dp.storage.update_data(user=call.from_user.id, data={"num": num + 3})
