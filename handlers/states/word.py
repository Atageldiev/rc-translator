from aiogram.types import Message, ChatActions, \
    ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from loader import dp, db, parser
from data.config import LANGS, ALLOWED_LANGS
from utils import Word

@dp.message_handler(state=Word.dest)
async def state_dest(message: Message, state: FSMContext):
    src = message.text
    await ChatActions.typing()

    if src in LANGS:
        user_id = message.from_user.id
        markup = ReplyKeyboardMarkup(
            resize_keyboard=True, row_width=3, one_time_keyboard=True)

        for element in ALLOWED_LANGS.get(src):
            markup.insert(element)

        await message.answer("Выберите язык <b><u>на который</u></b> хотите перевести", reply_markup=markup)
        await state.update_data(src=src)
        await Word.next()
    else:
        await message.answer("ERROR, TRY AGAIN\n/word", reply_markup=ReplyKeyboardRemove())
        await state.finish()

@dp.message_handler(state=Word.word)
async def state_word(message: Message, state: FSMContext):
    user_id = message.from_user.id

    data = await state.get_data()

    src = data["src"]
    dest = message.text

    await ChatActions.typing()

    if dest in ALLOWED_LANGS.get(src):
        await Word.next()
        await state.update_data(dest=message.text)

        await message.answer("Напишите слово, которое хотите перевести",
                             reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("ERROR, A SUPPORTED LANGUAGE IS REQUIRED\n/word",
                             reply_markup=ReplyKeyboardRemove())
        await state.finish()

@dp.message_handler(state=Word.res)
async def state_send_result(message: Message, state: FSMContext):
    user_id = message.from_user.id

    db.update_value(name="words_translated")

    await state.update_data(word=message.text)
    data = await state.get_data()
    
    text, markup = parser.parse_translations(data)
    
    await ChatActions.typing()
    await message.answer(text=text, reply_markup=markup)
    await state.reset_state(with_data=False)
