import logging

from loader import dp, bot
from data.config import ADMIN_ID
from utils.utils import AdminStates



async def command_users(message):
    users = []
    for el in db.get_user_ids():
        user_id = el[0]
        users.append(user_id)
    await answer_by_chat_id(chat_id=ADMIN_ID, text=f"Батя, бот ща насчитывает:---   <b>{len(users)}</b>   ---пользователей")

async def command_send_one(message):
    message = message.text.split("!send_one").pop(-1).split("/")
    await bot.send_message(chat_id=message[0].strip(" "), text=f"My father @t2elzeth says: \n'<em>{message[1]}</em>'")

async def command_send_log(message):
    logging.info("Log file has been sent")
    with open("mylog.log", "rb") as logFile:
        await bot.send_document(ADMIN_ID, logFile, caption="Вот логи, бать")

async def command_send_all(message):
    state = dp.current_state(user=message.from_user.id)
    await message.answer("Бать, напиши сообщение, которое хочешь отправить всем юзерам")

    await state.set_state(AdminStates.all()[0])

async def state_send_message_all(message):
    for el in db.get_user_ids():
        user_id = el[0]
        await bot.send_message(chat_id=user_id, text=message.text)

    await bot.send_message(chat_id=ADMIN_ID, text="Бать, я закончил")
    await state.reset_state()

async def command_setDB(message):
    state = dp.current_state(user=message.from_user.id)

    await message.answer("Отправьте файл, который надо загрузить")
    await state.set_state(AdminStates.all()[1])

async def state_setDB(message):
    try:
        info = await bot.get_file(message.document.file_id)
        await bot.download_file(file_path=info.file_path, destination="data/databases/server.db")
    except:
        await message.answer("Бать, чет пошло не так")

async def empty_messages(message):
    from_user = message.from_user

    await bot.send_message(chat_id=ADMIN_ID, text=f"<b>{from_user.first_name}</b> says:\n'<em>{message.text}</em>'\nuser_id:{from_user.id}",
                           disable_notification=True)
