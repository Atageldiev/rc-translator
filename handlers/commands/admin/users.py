from aiogram.types import Message

from core.conf import dp, bot, ADMINS
from utils.database import db
from utils.decorators import typing_action


@dp.message_handler(lambda message: message.from_user.id in ADMINS, commands="users", commands_prefix="!")
@typing_action
async def users(message: Message):
    for admin in ADMINS:
        await bot.send_message(chat_id=admin,
                               text=f"Батя, бот ща насчитывает:---   <b>{len(db.user_ids)}</b>   ---пользователей")
