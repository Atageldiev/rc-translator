from aiogram.types import ChatActions, Message
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db


@dp.message_handler(commands="start")
async def start(message: Message):
    db.user_id_exists()

    await ChatActions.typing()
    await message.reply("Привет, это бот для поиска переводов для различных слов\n/word\n/sentence")
