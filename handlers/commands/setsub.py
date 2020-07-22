from aiogram.types import Message, ChatActions, \
    InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, db

@dp.message_handler(commands="setsub")
async def setsub(message: Message):
    db.user_id_exists()

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        text="Subscribe/unsubscribe", callback_data="sub_unsub"))
    markup.add(InlineKeyboardButton(
        text="Change learning mode", callback_data="learning_mode"))

    await ChatActions.typing()
    await message.answer("Что вы хотите сделать?", reply_markup=markup)
