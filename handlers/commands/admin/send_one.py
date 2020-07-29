from aiogram.types import Message, ChatActions
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from data.config import ADMIN_ID
from utils import Admin


@dp.message_handler(lambda message: message.from_user.id == ADMIN_ID, commands="send_one", commands_prefix="!")
async def send_one(message: Message):
    await Admin.message_one_chat_id.set()
    await ChatActions.typing()
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
    await bot.forward_message(chat_id=data["message_one_chat_id"], from_chat_id=ADMIN_ID, message_id=message.message_id)
    await bot.send_message(chat_id=ADMIN_ID, text="Бать, я отправил")
    await state.reset_state()
