import logging

from aiogram.types import Message

from core.conf import settings
from loader import dp, db, bot
from utils.decorators import typing_action


@dp.message_handler(lambda message: message.from_user.id in settings.ADMINS, commands="users", commands_prefix="!")
@typing_action
async def users(message: Message):
    logging.info("Админ комманд ехекутед")
    users = db.get_user_ids()

    for admin in settings.ADMINS:
        await bot.send_message(chat_id=admin,
                               text=f"Батя, бот ща насчитывает:---   <b>{len(users)}</b>   ---пользователей")
