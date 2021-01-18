from aiogram.types import Message

from library.formatters import bold_underlined, cursive
from library.handlers.class_based import CommandHandler
from utils.database import db
from utils.decorators import typing_action, check_user_existance


class RatingHandler(CommandHandler):
    decorators = [typing_action, check_user_existance]

    async def handle(self, message: Message):
        name = message.from_user.first_name
        words_translated = db.words_translated
        grammar_used = db.grammar_used

        await message.answer(f"{bold_underlined(name)}, ваша статистика:\n"
                             f"     {cursive('Слов переведено')} - {words_translated}\n"
                             f"     {cursive('Помощника по грамматике использовано')} - {grammar_used}")
