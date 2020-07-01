# import from my files
from myclass import Parser
from loader import db

async def show_examples(callback_query):
    user_id = callback_query.from_user.id  

    word = db.get_value(name="word", user_id=user_id)
    lang_from = db.get_value(name="lang_from", user_id=user_id)
    lang_into = db.get_value(name="lang_into", user_id=user_id)

    await callback_query.answer("Обрабатываю...")

    await Parser.parse(callback_query.message, word, lang_from, lang_into, state=2)