
from aiogram import types
from aiogram.types import Message, ChatActions
from aiogram.dispatcher import FSMContext

from loader import dp, db, parser, translator
from data.config import LANGS, ALLOWED_LANGS, LANGCODES
from utils import WordStates, LearningMode, SentenceStates

@dp.message_handler(state=WordStates.dest)
async def state_dest(message: Message, state: FSMContext):
    src = message.text
    await ChatActions.typing()

    if src in LANGS:
        user_id = message.from_user.id
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, row_width=3, one_time_keyboard=True)

        for element in ALLOWED_LANGS.get(src):
            markup.insert(element)

        await message.answer("Выберите язык <b><u>на который</u></b> хотите перевести", reply_markup=markup)
        await state.update_data(src=src)
        await WordStates.next()
    else:
        await message.answer("ERROR, TRY AGAIN\n/word", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()

@dp.message_handler(state=WordStates.word)
async def state_word(message: Message, state: FSMContext):
    user_id = message.from_user.id

    data = await state.get_data()

    src = data["src"]
    dest = message.text

    await ChatActions.typing()

    if dest in ALLOWED_LANGS.get(src):
        await WordStates.next()
        await state.update_data(dest=message.text)

        await message.answer("Напишите слово, которое хотите перевести",
                             reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("ERROR, A SUPPORTED LANGUAGE IS REQUIRED\n/word",
                             reply_markup=types.ReplyKeyboardRemove())
        await state.finish()

@dp.message_handler(state=WordStates.res)
async def state_send_result(message: Message, state: FSMContext):
    user_id = message.from_user.id
    words_translated = db.get_value("words_translated", user_id)

    db.update_value(name="words_translated", value=words_translated + 1, user_id=user_id)

    await state.update_data(word=message.text)
    data = await state.get_data()

    await ChatActions.typing()
    await parser.parse_translations(data, message)
    await state.reset_state(with_data=False)

@dp.message_handler(state=LearningMode.mode)
async def state_choose_learningMode(message: Message, state: FSMContext):

    user_id = message.from_user.id
    markup = types.ReplyKeyboardRemove()

    await ChatActions.typing()
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


@dp.message_handler(state=SentenceStates.dest)
async def state_sentence(message: Message, state: FSMContext):
    text = message.text

    await ChatActions.typing()
    if text in LANGS:
        await state.update_data(src=LANGCODES.get(text))
        markup = types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True, resize_keyboard=True)
        for el in LANGS:
            markup.insert(el)
        await message.answer("Выберите язык <b><u>на который</u></b> хотите перевести", reply_markup=markup)
        await SentenceStates.next()
    else:
        await message.answer("ERROR, A SUPPORTED LANGUAGE IS REQUIRED\n/sentence",
                             reply_markup=types.ReplyKeyboardRemove())
        await state.finish()

@dp.message_handler(state=SentenceStates.sentence)
async def state_sentence(message: Message, state: FSMContext):
    await ChatActions.typing()

    if message.text in LANGS:
        await state.update_data(dest=LANGCODES.get(message.text))
        await message.answer("Напишите предложение")
        await SentenceStates.next()
    else:
        await message.answer("ERROR, A SUPPORTED LANGUAGE IS REQUIRED\n/sentence",
                             reply_markup=types.ReplyKeyboardRemove())
        await state.finish()

@dp.message_handler(state=SentenceStates.res)
async def state_sentence(message: Message, state: FSMContext):
    await state.update_data(sentence=message.text)
    await ChatActions.typing()

    data = await state.get_data()

    text = translator.translate(data["sentence"], src=data["src"], dest=data["dest"]).text

    await message.answer(f"<b>Вот результаты:</b> \n\n<em>'{text}'</em>", reply_markup=types.ReplyKeyboardRemove())
    await state.reset_state(with_data=False)
        
