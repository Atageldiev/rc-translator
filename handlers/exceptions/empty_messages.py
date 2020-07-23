from aiogram.types import Message, ChatActions

from loader import dp
from modules import get_translation
from data.config import LANGCODES

@dp.message_handler()
async def empty_messages(message: Message):
    data = await dp.storage.get_data(user=message.from_user.id)
    msg = message.text

    await ChatActions.typing()
    if data:
        dest = data["dest"]
        res = get_translation(msg, data=data)

        await message.answer(f"<b><u>Вы в последний раз переводили:</u></b>\n\
    <b>На язык</b> - {dest}\n\
    <b>Результат:</b> \n\n\
        <em>'{res}'</em>\n\n/sentence\n/reset - чтобы сбросить")
    else:
        res_ru = get_translation(text=msg, dest="ru")
        res_en = get_translation(text=msg, dest="en")
        res_fr = get_translation(text=msg, dest="fr")
        res_de = get_translation(text=msg, dest="de")
        res_es = get_translation(text=msg, dest="es")

        await message.answer(f"Результаты:\n\
    <b>Русский</b>  - {res_ru}\n\
    <b>English</b>  - {res_en}\n\
    <b>Français</b> - {res_fr}\n\
    <b>Deutsch</b>  - {res_de}\n\
    <b>Español</b>  - {res_es}\n\n/sentence")
