from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import Message, ReplyKeyboardRemove

from core.settings import dp, storage
from core.commands.common import COMMAND_CANCEL
from utils.decorators import typing_action


@dp.message_handler(Command(COMMAND_CANCEL), state="*")
@dp.message_handler(lambda message: message.text.lower().strip() in ('cancel',))
@typing_action
async def cancel(message: Message, *args, **kwargs):
    await storage.reset_state(user=message.from_user.id)
    await message.reply("Cancelled...", reply_markup=ReplyKeyboardRemove())
