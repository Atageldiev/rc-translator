from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from core.settings import dp
from core.commands.common import COMMAND_RATING
from core.database import db
from utils.text import FormattedText


@dp.message_handler(Command(COMMAND_RATING))
async def handle_rating(message: Message):
    await message.answer(f"{FormattedText(message.from_user.first_name).bold().underlined()}, ваша статистика:\n"
                         f"     {FormattedText('Слов переведено').cursive()} - {db.translated}\n"
                         f"     {FormattedText('Помощника по грамматике использовано').cursive()} - {db.grammar_used}")
