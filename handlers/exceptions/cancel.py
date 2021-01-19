from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import Message, ReplyKeyboardRemove

from core.conf import dp, storage
from utils.decorators import typing_action


@dp.message_handler(Command("cancel"), state="*")
@dp.message_handler(lambda message: message.text.lower().strip() in ('cancel',))
@typing_action
async def cancel(message: Message):
    await storage.reset_state(user=message.from_user.id)
    await message.reply("Cancelled...", reply_markup=ReplyKeyboardRemove())
