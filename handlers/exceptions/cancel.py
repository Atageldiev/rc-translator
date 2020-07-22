from aiogram.types import ChatActions, Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db


@dp.message_handler(commands="cancel")
@dp.message_handler(lambda message: message.text.lower() == "cancel")
async def cancel(message: Message):
    await ChatActions.typing()
    await dp.storage.reset_state(user=message.from_user.id)
    await message.reply("Cancelled...", reply_markup=None)
    await message.reply("Keyboard removed", reply_markup=ReplyKeyboardRemove())
