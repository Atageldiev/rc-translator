from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from core.conf import dp
from utils.database import db
from utils.decorators import typing_action, check_user_existance


@dp.message_handler(Command("rating"))
@typing_action
@check_user_existance
async def rating(message: Message):
    name = message.from_user.first_name
    words_translated = db.get_value(name="words_translated")
    grammar_used = db.get_value(name="grammar_used")

    await message.answer(f"<b><u>{name}</u></b>, ваша статистика:\n\
    <em>Слов переведено:</em>- {words_translated}\n \
    <em>Помощника по грамматике использовано:</em>- {grammar_used}")
