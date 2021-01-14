import logging

from aiogram.types import Message, ChatActions

from core.conf import dp, bot, settings


@dp.message_handler(lambda message: message.from_user.id in settings.ADMINS, commands="send_log", commands_prefix="!")
async def send_log(message: Message):
    logging.info("Log file has been sent")
    await ChatActions.upload_document()
    with open("data/bot.log", "rb") as logFile:
        for admin in settings.ADMINS:
            await bot.send_document(admin, logFile, caption="Вот логи, бать")
