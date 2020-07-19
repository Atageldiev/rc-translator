#---------------------------------------------------------------------------
#   imports
#---------------------------------------------------------------------------
import logging

from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loader import dp, db, bot
from data.config import ADMIN_ID
from utils.utils import AdminStates


#---------------------------------------------------------------------------
#   Functions
#---------------------------------------------------------------------------
@dp.message_handler(lambda message: message.from_user.id == ADMIN_ID, commands="users", commands_prefix="!")
async def users(message: Message):
    users = []
    for el in db.get_user_ids():
        user_id = el[0]
        users.append(user_id)
    await bot.send_message(chat_id=ADMIN_ID, text=f"Батя, бот ща насчитывает:---   <b>{len(users)}</b>   ---пользователей")


@dp.message_handler(lambda message: message.from_user.id == ADMIN_ID, commands="send_one", commands_prefix="!")
async def send_one(message: Message):
    await AdminStates.message_one_chat_id.set()
    await message.answer("Бать, скинь chat_id")


@dp.message_handler(lambda message: message.from_user.id == ADMIN_ID, commands="send_log", commands_prefix="!")
async def send_log(message: Message):
    logging.info("Log file has been sent")
    with open("data/bot.log", "rb") as logFile:
        await bot.send_document(ADMIN_ID, logFile, caption="Вот логи, бать")

@dp.message_handler(lambda message: message.from_user.id == ADMIN_ID, commands="send_db", commands_prefix="!")
async def send_log(message: Message):
    logging.info("Log file has been sent")
    with open("data/server.db", "rb") as logFile:
        await bot.send_document(ADMIN_ID, logFile, caption="Вот БД, бать")


@dp.message_handler(lambda message: message.from_user.id == ADMIN_ID, commands="send_all", commands_prefix="!")
async def send_all(message: Message):
    await AdminStates.send_message_all.set()
    await message.answer("Бать, напиши сообщение, которое хочешь отправить всем юзерам")

@dp.message_handler(lambda message: message.from_user.id == ADMIN_ID, commands="setDB", commands_prefix="!")
async def setDB(message: Message):
    state = dp.current_state(user=message.from_user.id)

    await message.answer("Отправьте файл, который надо загрузить")
    await state.set_state(AdminStates.setDB)

@dp.message_handler(lambda message: message.from_user.id != ADMIN_ID)
async def empty_messages(message: Message):
    from_user = message.from_user

    await bot.send_message(chat_id=ADMIN_ID, text=f"<b>{from_user.first_name}</b> says:\n'<em>{message.text}</em>'\nuser_id:{from_user.id}",
                           disable_notification=True)


#---------------------------------------------------------------------------
#   States
#---------------------------------------------------------------------------
@dp.message_handler(state=AdminStates.send_message_all)
async def state_send_message_all(message: Message, state: FSMContext):
    for el in db.get_user_ids():
        user_id = el[0]
        await bot.send_message(chat_id=user_id, text=message.text)

    await bot.send_message(chat_id=ADMIN_ID, text="Бать, я закончил")
    await state.reset_state()


@dp.message_handler(state=AdminStates.setDB, content_types="document")
async def state_setDB(message: Message, state: FSMContext):
    info = await bot.get_file(message.document.file_id)
    await bot.download_file(file_path=info.file_path, destination="data/server.db")
    await message.answer("Бать, я сохранил БД")
    await state.reset_state()


@dp.message_handler(state=AdminStates.setDB)
async def state_setDB_error(message: Message, state: FSMContext):
    await message.answer("Бать, чет пошло не так")
    await state.reset_state()

@dp.message_handler(state=AdminStates.message_one_chat_id)
async def state_setDB_error(message: Message, state: FSMContext):
    await state.update_data(message_one_chat_id=message.text)
    await message.answer("Бать, какое сообщ отправить?")
    await AdminStates.next()
    
@dp.message_handler(state=AdminStates.message_one_text)
async def state_setDB_error(message: Message, state: FSMContext):
    await state.update_data(message_one_text=message.text)
    data = await state.get_data()
    await bot.forward_message(chat_id=data["message_one_chat_id"], from_chat_id=ADMIN_ID, message_id=message.message_id)
    await bot.send_message(chat_id=ADMIN_ID, text="Бать, я отправил")
    await state.reset_state()
