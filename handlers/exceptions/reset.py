from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import Message

from core.conf.settings import dp
from utils.decorators import typing_action


@dp.message_handler(Command("reset"))
@dp.message_handler(text=("Cancel", "cancel"))
@typing_action
async def cancel(message: Message):
    await dp.storage.reset_state(user=message.from_user.id)
    await message.reply("Success")
