# import from required libraries
import asyncio
import schedule

# import from my files
from loader import bot
from config import saveDB
from telebot_addon.mymodule import backUpDB

async def answer_by_chat_id(chat_id, text, disable_notification=False):
    return await bot.send_message(chat_id=chat_id, text=text, disable_notification=disable_notification)


async def backUpDB_task():
    schedule.every().day.at("01:55").do(backUpDB)
    while 1:
        schedule.run_pending()
        await asyncio.sleep(1)

async def saveDoc(document):
    info = await bot.get_file(document.file_id)
    await bot.download_file(file_path=info.file_path, destination="server.db")
