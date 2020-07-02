# import from my files
from loader import bot


async def answer_by_chat_id(chat_id, text):
    return await bot.send_message(chat_id=chat_id, text=text)
    await bot.send_document
