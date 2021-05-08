from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from core.settings import dp, bot, ADMINS
from core.commands.admin import COMMAND_SEND_ALL
from core.database import db
from core.states import Admin
from utils.decorators import typing_action


@dp.message_handler(lambda message: message.from_user.id in ADMINS, commands=COMMAND_SEND_ALL, commands_prefix="!")
@typing_action
async def send_all(message: Message, *args, **kwargs):
    await Admin.send_message_all.set()
    await message.answer("Бать, напиши сообщение, которое хочешь отправить всем юзерам")


@dp.message_handler(state=Admin.send_message_all)
async def state_send_message_all(message: Message, state: FSMContext):
    for el in db.user_ids:
        await bot.send_message(chat_id=el, text=message.text)

    for admin in ADMINS:
        await bot.send_message(chat_id=admin, text="Бать, я закончил")
    await state.reset_state()
