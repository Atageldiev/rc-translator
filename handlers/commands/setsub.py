from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import (
    CallbackQuery, Message,
    ReplyKeyboardRemove, ReplyKeyboardMarkup
)

from core.conf.settings import dp
from core.states import LearningModeState
from utils.buttons import get_ikb
from core.database import db
from utils.decorators import typing_action, check_user_existance
from core.conf.learning_mode import LearningMode


@dp.message_handler(Command("setsub"))
@typing_action
@check_user_existance
async def setsub(message: Message):
    await message.answer("Что вы хотите сделать?",
                         reply_markup=get_ikb([{"text": "Subscribe/unsubscribe", "callback_data": "sub_unsub"},
                                               {"text": "Change learning mode", "callback_data": "learning_mode"}]))


@dp.callback_query_handler(text="sub_unsub")
async def sub_unsub(call: CallbackQuery):
    status = LearningMode.STATUSES.get(db.subbed)
    await call.message.edit_text(f"Ваш активный статус: <em>{status}</em>",
                                 reply_markup=get_ikb([{"text": "Subscribe", "callback_data": "sub"},
                                                       {"text": "Unsubscribe", "callback_data": "unsub"}]))


@dp.callback_query_handler(text="sub")
async def sub(call: CallbackQuery):
    db.subbed = True
    await call.answer("Success!")
    await call.message.edit_text(f"Ваш активный статус: <em>{LearningMode.STATUSES.get(db.subbed)}/em>")


@dp.callback_query_handler(text="unsub")
async def unsub(call: CallbackQuery):
    db.subbed = False
    await call.answer("Success!")
    await call.message.edit_text(f"Ваш активный статус: <em>{LearningMode.STATUSES.get(db.subbed)}</em>")


@dp.callback_query_handler(text="learning_mode")
async def learning_mode(call: CallbackQuery):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    for el in LearningMode.MODES.keys():
        markup.insert(LearningMode.PREFIX + el)
    markup.add("Cancel")

    await call.message.reply(
        f"Доступные режимы обучения: \n\n1 - {LearningMode.MODES.get(1)}\n2 - {LearningMode.MODES.get(2)}\n\n"
        f"<b>Внимание!</b>\nВремя в каждом режиме прописано по Бишкекскому\n(GMT+06)")
    await call.message.reply(
        f"Ваш активный режим обучения: <em>{db.learning_mode}</em>\n\n"
        f"<em><u>Нажмите на соответствующую кнопку, чтобы изменить режим</u></em>",
        reply_markup=markup)
    await LearningModeState.mode.set()


@dp.message_handler(state=LearningModeState.mode)
async def choose_learning_mode(message: Message, state: FSMContext):
    mode = int(message.text.removeprefix(LearningMode.PREFIX))
    await set_and_notify_learning_mode(mode, message)
    await state.finish()


async def set_and_notify_learning_mode(mode: int, message):
    if mode not in LearningMode.MODES.keys():
        return await message.answer("ERROR, TRY AGAIN\n/setsub", reply_markup=ReplyKeyboardRemove())

    db.learning_mode = mode
    await message.answer(f"Ваш активный режим обучения: <em> {LearningMode.MODES.get(mode)}</em>",
                         reply_markup=ReplyKeyboardRemove())
