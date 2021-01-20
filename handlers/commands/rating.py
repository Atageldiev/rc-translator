from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from core.conf.settings import dp
from core.database import db
from utils.formatters import bold_underlined, cursive


@dp.message_handler(Command("rating"))
async def handle_rating(message: Message):
    await message.answer(f"{bold_underlined(message.from_user.first_name)}, ваша статистика:\n"
                         f"     {cursive('Слов переведено')} - {db.translated}\n"
                         f"     {cursive('Помощника по грамматике использовано')} - {db.grammar_used}")
