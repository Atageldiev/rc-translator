from aiogram.types import Message, ChatActions

from loader import dp, translator


@dp.message_handler()
async def empty_messages(message: Message):
    data = await dp.storage.get_data(user=message.from_user.id)
    msg = message.text

    await ChatActions.typing()
    try:
        src = data["src"]
        dest = data["dest"]
        res = translator.translate(text=msg, dest=dest, src=src).text

        await message.answer(f"<b><u>Вы последний раз переводили:</u></b>\n\
    <b>С языка</b> - {src}\n\
    <b>На язык</b> - {dest}\n\
    <b>Результат:</b> \n\n\
        <em>'{res}'</em>\n\n/sentence")
    except:
        res_ru = translator.translate(text=msg, dest="ru").text
        res_en = translator.translate(text=msg, dest="en").text
        res_fr = translator.translate(text=msg, dest="fr").text
        res_de = translator.translate(text=msg, dest="de").text
        res_es = translator.translate(text=msg, dest="es").text

        await message.answer(f"Результаты:\n\
    <b>Русский</b>  - {res_ru}\n\
    <b>English</b>  - {res_en}\n\
    <b>Français</b> - {res_fr}\n\
    <b>Deutsch</b>  - {res_de}\n\
    <b>Español</b>  - {res_es}\n\n/sentence")
