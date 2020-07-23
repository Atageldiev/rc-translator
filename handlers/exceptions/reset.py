from aiogram.types import (
    Message, ChatActions
)
from aiogram.dispatcher.filters.builtin import Command

from loader import dp


@dp.message_handler(Command("reset"))
@dp.message_handler(text=("Cancel", "cancel"))
async def cancel(message: Message):
    await ChatActions.typing()
    await dp.storage.reset_state(user=message.from_user.id)
    await message.reply("Success")
