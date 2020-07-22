#---------------------------------------------------------------------------
#   imports
#---------------------------------------------------------------------------
import logging

from aiogram.types import Message, ChatActions, ContentType

from loader import dp

#---------------------------------------------------------------------------
#   Handlers
#---------------------------------------------------------------------------
@dp.message_handler(content_types=[ContentType.DOCUMENT, ContentType.PHOTO, 
                                    ContentType.AUDIO, ContentType.VOICE, ContentType.VIDEO
                                    ])
async def other_types(message: Message):
    await ChatActions.typing()
    await message.answer("Ну и что мне с этим сделать? 😒")
