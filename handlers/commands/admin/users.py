import logging

from aiogram.types import Message

from core.conf import settings
from loader import dp, db, bot
from utils.decorators import typing_action

ADMIN_ID = settings.ADMIN_ID


@dp.message_handler(lambda message: message.from_user.id == ADMIN_ID, commands="users", commands_prefix="!")
@typing_action
async def users(message: Message):
    logging.info("Админ комманд ехекутед")
    users = db.get_user_ids()
    await bot.send_message(chat_id=ADMIN_ID,
                           text=f"Батя, бот ща насчитывает:---   <b>{len(users)}</b>   ---пользователей")
