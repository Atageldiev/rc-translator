from aiogram.types import Message

from library.formatters import bold_underlined, cursive
from library.handlers.class_based import CommandHandler
from utils.database import db
from utils.decorators import typing_action, check_user_existance


class RatingHandler(CommandHandler):
    decorators = [typing_action, check_user_existance]
    commands = ["rating"]

    async def handle(self, message: Message):
        await message.answer(f"{bold_underlined(message.from_user.first_name)}, ваша статистика:\n"
                             f"     {cursive('Слов переведено')} - {db.translated}\n"
                             f"     {cursive('Помощника по грамматике использовано')} - {db.grammar_used}")
