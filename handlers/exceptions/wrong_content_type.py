from aiogram.types import Message, ContentType

from core.conf import dp
from utils.decorators import typing_action


@dp.message_handler(content_types=[ContentType.DOCUMENT, ContentType.PHOTO,
                                   ContentType.AUDIO, ContentType.VOICE, ContentType.VIDEO, ContentType.STICKER])
@typing_action
async def other_types(message: Message):
    await message.answer("Ну и что мне с этим сделать? 😒")
