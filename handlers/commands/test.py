from aiogram.types import ChatActions, Message
from aiogram.dispatcher.filters.builtin import Command

from loader import dp
from data.config import ADMIN_ID


@dp.message_handler(Command("test"))
async def cmd_test(message: Message):
    await ChatActions.typing()
    await message.answer("Это тестовое сообщение")