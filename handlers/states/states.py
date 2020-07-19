
from aiogram import types
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loader import dp, db, Parser
from data.config import LANGS, ALLOWED_LANGS
from utils.utils import WordStates, LearningMode

@dp.message_handler(state=WordStates.lang_into)
async def state_lang_into(message: Message, state: FSMContext):
    lang_from = message.text
    if lang_from in LANGS:
        user_id = message.from_user.id
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, row_width=3, one_time_keyboard=True)

        for element in ALLOWED_LANGS.get(lang_from):
            markup.insert(element)

        await message.answer("Выберите язык <b><u>на который</u></b> хотите перевести", reply_markup=markup)
        await state.update_data(lang_from=lang_from)
        await WordStates.next()
    else:
        await message.answer("ERROR, TRY AGAIN\n/translate", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()

@dp.message_handler(state=WordStates.word)
async def state_word(message: Message, state: FSMContext):

    user_id = message.from_user.id
    data = await state.get_data()
    lang_from = data["lang_from"]
    lang_into = message.text

    if lang_into in ALLOWED_LANGS.get(lang_from):
        await WordStates.next()
        await state.update_data(lang_into=message.text)

        await message.answer("Напишите слово, которое хотите перевести",
                             reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("ERROR, TRY AGAIN\n/translate",
                             reply_markup=types.ReplyKeyboardRemove())
        await state.finish()

@dp.message_handler(state=WordStates.res)
async def state_send_result(message: Message, state: FSMContext):
    user_id = message.from_user.id
    words_translated = db.get_value("words_translated", user_id)

    db.update_value(name="words_translated", value=words_translated + 1, user_id=user_id)

    await state.update_data(word=message.text)
    data = await state.get_data()
    await Parser.parse(message, data, level=1)
    await state.reset_state(with_data=False)

@dp.message_handler(state=LearningMode.mode)
async def state_choose_learningMode(message: Message, state: FSMContext):

    user_id = message.from_user.id
    markup = types.ReplyKeyboardRemove()

    if message.text == "Mode 1":
        db.update_value("learning_mode", 1, user_id)
        status = "10:00 | 14:00 | 18:00"
        await message.answer(f"Ваш активный режим обучения: <em> {status}</em>", reply_markup=markup)

    elif message.text == "Mode 2":
        db.update_value("learning_mode", 2, user_id)
        status = "10:00 | 13:00 | 16:00"
        await message.answer(f"Ваш активный режим обучения: <em> {status}</em>", reply_markup=markup)

    elif message.text == "Mode 3":
        db.update_value("learning_mode", 3, user_id)
        status = "10:00 | 15:00 | 20:00"
        await message.answer(f"Ваш активный режим обучения: <em> {status}</em>", reply_markup=markup)

    elif message.text == "Cancel":
        await message.answer("Cancelled", reply_markup=markup)

    else:
        await message.answer("ERROR, TRY AGAIN\n/setsub", reply_markup=markup)

    await state.finish()

