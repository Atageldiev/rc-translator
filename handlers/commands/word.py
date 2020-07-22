from aiogram.types import Message, ChatActions, ReplyKeyboardMarkup

from loader import dp, db
from data.config import LANGS
from utils import Word

@dp.message_handler(commands="word")
async def translate(message: Message):
    await dp.storage.update_data(user=message.from_user.id, data={"num": 3})

    db.user_id_exists()

    markup = ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=3, one_time_keyboard=True)

    for element in LANGS:
        markup.insert(element)

    await ChatActions.typing()
    await Word.dest.set()
    await message.answer("Выберите язык <b><u>с которого</u></b> хотите перевести", reply_markup=markup)
