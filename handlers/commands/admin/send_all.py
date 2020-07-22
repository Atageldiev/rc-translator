from aiogram.types import Message, ChatActions
from aiogram.dispatcher import FSMContext

from loader import dp, db, bot
from data.config import ADMIN_ID
from utils import Admin

@dp.message_handler(lambda message: message.from_user.id == ADMIN_ID, commands="send_all", commands_prefix="!")
async def send_all(message: Message):
    await Admin.send_message_all.set()
    await ChatActions.typing()
    await message.answer("Бать, напиши сообщение, которое хочешь отправить всем юзерам")


@dp.message_handler(state=Admin.send_message_all)
async def state_send_message_all(message: Message, state: FSMContext):
    for el in db.get_user_ids():
        user_id = el[0]
        await bot.send_message(chat_id=user_id, text=message.text)

    await bot.send_message(chat_id=ADMIN_ID, text="Бать, я закончил")
    await state.reset_state()
