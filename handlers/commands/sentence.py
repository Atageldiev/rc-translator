from aiogram.types import Message, ReplyKeyboardMarkup,\
    ChatActions

from loader import dp, db
from data.config import LANGS
from utils import Sentence

@dp.message_handler(commands="sentence")
async def sentence(message: Message):
    db.user_id_exists()
    markup = ReplyKeyboardMarkup(
        row_width=3, one_time_keyboard=True, resize_keyboard=True)
    for el in LANGS:
        markup.insert(el)

    await ChatActions.typing()
    await message.answer("Выберите язык <b><u>с которого</u></b> хотите перевести", reply_markup=markup)
    await Sentence.dest.set()
