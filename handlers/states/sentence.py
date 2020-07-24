from aiogram.types import Message, ChatActions, \
    ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from loader import dp, db
from modules import get_translation
from data.config import LANGS, LANGCODES
from utils import Sentence

@dp.message_handler(state=Sentence.dest)
async def state_sentence(message: Message, state: FSMContext):
    text = message.text
    
    await ChatActions.typing()
    if text in LANGS:
        await state.update_data(src=text)
        markup = ReplyKeyboardMarkup(
            row_width=3, one_time_keyboard=True, resize_keyboard=True)
        for el in LANGS:
            markup.insert(el)
        await message.answer("Выберите язык <b><u>на который</u></b> хотите перевести", reply_markup=markup)
        await Sentence.next()
    else:
        await message.answer("ERROR, A SUPPORTED LANGUAGE IS REQUIRED\n/sentence",
                             reply_markup=ReplyKeyboardRemove())
        await state.finish()


@dp.message_handler(state=Sentence.sentence)
async def state_sentence(message: Message, state: FSMContext):
    await ChatActions.typing()
    text = message.text
    if text in LANGS:
        await state.update_data(dest=text)
        await message.answer("Напишите предложение")
        await Sentence.next()
    else:
        await message.answer("ERROR, A SUPPORTED LANGUAGE IS REQUIRED\n/sentence",
                             reply_markup=ReplyKeyboardRemove())
        await state.finish()


@dp.message_handler(state=Sentence.res)
async def state_sentence(message: Message, state: FSMContext):
    sentence = message.text
    await ChatActions.typing()

    data = await state.get_data()
    text = get_translation(sentence, data=data)

    await message.answer(f"<b>Вот результаты:</b> \n\n<em>'{text}'</em>", reply_markup=ReplyKeyboardRemove())
    await state.reset_state(with_data=False)
