from aiogram.types import Message, ChatActions
from aiogram.dispatcher.filters import Command

from loader import dp, db 


@dp.message_handler(Command("rating"))
async def rating(message: Message):
    user_id = message.from_user.id
    name = message.from_user.first_name

    db.user_id_exists()

    words_translated = db.get_value(name="words_translated")
    grammar_used = db.get_value(name="grammar_used")

    await ChatActions.typing()
    await message.answer(f"<b><u>{name}</u></b>, ваша статистика:\n\
    <em>Слов переведено:</em>- {words_translated}\n \
    <em>Помощника по грамматике использовано:</em>- {grammar_used}")
