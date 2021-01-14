from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import Message

from core.conf import dp
from utils.database import db
from utils.decorators import typing_action, check_user_existance
from .utils import get_markup_by_key_from_json


@dp.message_handler(Command("grammar"))
@typing_action
@check_user_existance
async def grammar(message: Message):
    db.grammar_used += 1

    markup = await get_markup_by_key_from_json("default")
    await message.answer("Выберите насчет чего вы хотите получить готовую информацию: ", reply_markup=markup)
