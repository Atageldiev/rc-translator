import logging

from aiogram.types import Message, ChatActions

from loader import dp, bot
from data.config import ADMIN_ID

@dp.message_handler(lambda message: message.from_user.id == ADMIN_ID, commands="send_db", commands_prefix="!")
async def send_log(message: Message):
    logging.info("DB file has been sent")
    await ChatActions.upload_document()
    with open("data/server.db", "rb") as logFile:
        await bot.send_document(ADMIN_ID, logFile, caption="Вот БД, бать")
