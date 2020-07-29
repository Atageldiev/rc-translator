from aiogram.types import (
    Message, ChatActions, 
    ReplyKeyboardRemove as RKR
    )
from aiogram.dispatcher.filters.builtin import Command, Text

from loader import dp


@dp.message_handler(Command("cancel"), state="*")
@dp.message_handler(text=("Cancel", "cancel"))
async def cancel(message: Message):
    await ChatActions.typing()
    await dp.storage.reset_state(user=message.from_user.id)
    await message.reply("Cancelled...", reply_markup=RKR())
    
