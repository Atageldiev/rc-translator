from aiogram.types import Message, ChatActions, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from loader import dp, db
from data.config import LEARNING_MODE
from utils import LearningMode

@dp.message_handler(state=LearningMode.mode)
async def choose_learning_mode(message: Message, state: FSMContext):

    user_id = message.from_user.id
    markup = ReplyKeyboardRemove()

    await ChatActions.typing()
    if message.text == "Mode 1":
        db.update_value("learning_mode", 1)
        status = LEARNING_MODE.get(1)
        await message.answer(f"Ваш активный режим обучения: <em> {status}</em>", reply_markup=markup)

    elif message.text == "Mode 2":
        db.update_value("learning_mode", 2)
        status = LEARNING_MODE.get(2)
        await message.answer(f"Ваш активный режим обучения: <em> {status}</em>", reply_markup=markup)

    # elif message.text == "Mode 3":
    #     db.update_value("learning_mode", 3)
    #     status = "10:00 | 15:00 | 20:00"
    #     await message.answer(f"Ваш активный режим обучения: <em> {status}</em>", reply_markup=markup)
    else:
        await message.answer("ERROR, TRY AGAIN\n/setsub", reply_markup=markup)

    await state.finish()
