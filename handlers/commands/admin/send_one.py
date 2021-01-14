from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from core.conf import settings
from loader import dp, bot
from utils import Admin
from utils.decorators import typing_action


@dp.message_handler(lambda message: message.from_user.id in settings.ADMINS, commands="send_one", commands_prefix="!")
@typing_action
async def send_one(message: Message):
    await Admin.message_one_chat_id.set()
    await message.answer("Бать, скинь chat_id")


@dp.message_handler(state=Admin.message_one_chat_id)
async def state_setDB_error(message: Message, state: FSMContext):
    await state.update_data(message_one_chat_id=message.text)
    await message.answer("Бать, какое сообщение отправить?")
    await Admin.next()


@dp.message_handler(state=Admin.message_one_text)
async def state_setDB_error(message: Message, state: FSMContext):
    await state.update_data(message_one_text=message.text)
    data = await state.get_data()

    for admin in settings.ADMINS:
        await bot.forward_message(chat_id=data["message_one_chat_id"],
                                  from_chat_id=admin,
                                  message_id=message.message_id)
        await bot.send_message(chat_id=admin, text="Бать, я отправил")
    await state.reset_state()
