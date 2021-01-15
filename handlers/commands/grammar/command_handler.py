from aiogram.types import Message

from library.handlers.class_based import CommandHandler
from utils.database import db
from utils.decorators import typing_action, check_user_existance
from .utils import get_markup_by_key_from_json


class GrammarHandler(CommandHandler):
    decorators = [typing_action, check_user_existance]

    async def handle(self, message: Message):
        db.grammar_used += 1

        markup = await get_markup_by_key_from_json("default")
        await message.answer("Выберите насчет чего вы хотите получить готовую информацию: ", reply_markup=markup)


class FuckYouBitchHandler(CommandHandler):
    decorators = [typing_action]

    async def handle(self, message: Message):
        await message.answer("GO FUCK YOURSELF YO BITCH!")
