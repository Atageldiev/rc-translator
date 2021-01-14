from aiogram.dispatcher.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup

from data.config import LANGS
from loader import dp, db
from utils import Sentence


@dp.message_handler(Command("sentence"))
async def sentence(message: Message):
    db.user_id_exists()

    markup = ReplyKeyboardMarkup(
        row_width=3,
        one_time_keyboard=True,
        resize_keyboard=True
    )

    for el in LANGS:
        markup.insert(el)

    await message.answer("Выберите язык с которого хотите перевести", reply_markup=markup)
    await Sentence.dest.set()
