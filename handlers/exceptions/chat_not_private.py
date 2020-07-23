import logging

from aiogram.types import (
    Message, ChatActions, 
    InlineKeyboardMarkup, InlineKeyboardButton,
    ChatType
    )

from loader import dp

@dp.message_handler(lambda message: not ChatType.is_private(message))
async def not_private(message: Message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
            text="ЛС тут", url="https://t.me/rc_translate_bot"))
    await ChatActions.typing()
    await message.answer("Бот работает только в лс", reply_markup=markup)
