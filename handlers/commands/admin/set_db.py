from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from core.conf import dp, bot, ADMINS
from utils import Admin
from utils.decorators import typing_action


@dp.message_handler(lambda message: message.from_user.id in ADMINS, commands="set_db", commands_prefix="!")
@typing_action
async def set_db(message: Message):
    state = dp.current_state(user=message.from_user.id)

    await message.answer("Отправьте файл, который надо загрузить")
    await state.set_state(Admin.setDB)


@dp.message_handler(state=Admin.setDB, content_types="document")
async def state_setDB(message: Message, state: FSMContext):
    info = await bot.get_file(message.document.file_id)
    await bot.download_file(file_path=info.file_path, destination="data/server.db")
    await message.answer("Бать, я сохранил БД")
    await state.reset_state()


@dp.message_handler(state=Admin.setDB)
async def state_setDB_error(message: Message, state: FSMContext):
    await message.answer("Бать, чет пошло не так")
    await state.reset_state()
