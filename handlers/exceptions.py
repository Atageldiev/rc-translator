#---------------------------------------------------------------------------
#   imports
#---------------------------------------------------------------------------
import logging

from aiogram import types
from aiogram.types import Message, ChatActions, ChatType, ContentType

from loader import dp

#---------------------------------------------------------------------------
#   Handlers
#---------------------------------------------------------------------------
@dp.message_handler(lambda message: not ChatType.is_private(message))
async def start(message: Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        text="ЛС тут", url="https://t.me/rc_translate_bot"))
    await ChatActions.typing()
    await message.answer("Бот работает только в лс", reply_markup=markup)

@dp.message_handler(content_types=[ContentType.DOCUMENT, ContentType.PHOTO, 
                                    ContentType.AUDIO, ContentType.VOICE, ContentType.VIDEO
                                    ])
async def process_other_types(message: Message):
    await ChatActions.typing()
    await message.answer("Ну и что мне с этим сделать? 😒")
