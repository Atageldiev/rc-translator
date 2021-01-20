from aiogram.types import Message, ChatActions

from core.conf.settings import dp, bot, ADMINS


@dp.message_handler(lambda message: message.from_user.id in ADMINS, commands="send_log", commands_prefix="!")
async def send_log(message: Message):
    await ChatActions.upload_document()
    with open("data/bot.log", "rb") as logFile:
        for admin in ADMINS:
            await bot.send_document(admin, logFile, caption="Вот логи, бать")
