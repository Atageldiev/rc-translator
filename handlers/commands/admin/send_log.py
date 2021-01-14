import logging

from aiogram.types import Message, ChatActions

from core.conf import settings
from loader import dp, bot


@dp.message_handler(lambda message: message.from_user.id == settings.ADMIN_ID, commands="send_log", commands_prefix="!")
async def send_log(message: Message):
    logging.info("Log file has been sent")
    await ChatActions.upload_document()
    with open("data/bot.log", "rb") as logFile:
        await bot.send_document(settings.ADMIN_ID, logFile, caption="Вот логи, бать")
