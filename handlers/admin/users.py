from aiogram.types import Message

from core.settings import dp, bot, ADMINS
from core.commands.admin import COMMAND_USERS
from core.database import db
from utils.decorators import typing_action


@dp.message_handler(lambda message: message.from_user.id in ADMINS, commands=COMMAND_USERS, commands_prefix="!")
@typing_action
async def users(*args, **kwargs):
    for admin in ADMINS:
        await bot.send_message(chat_id=admin,
                               text=f"Батя, бот ща насчитывает:---   <b>{len(db.user_ids)}</b>   ---пользователей")
