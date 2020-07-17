# import from required libraries
import asyncio
import schedule
import telebot
import logging 

from datetime import datetime
from aiogram import executor

# import from my files
from data.config import chatSaveDB, TOKEN

teleBot = telebot.TeleBot(TOKEN)
    
def BackUp():
    with open("data/server.db", "rb") as dbFile, open("mylog.log", "rb") as logFile:
        teleBot.send_document(chat_id=chatSaveDB, data=dbFile, caption=f"База данных на {datetime.now()}")
        teleBot.send_document(chat_id=chatSaveDB, data=logFile, caption=f"Логи на {datetime.now()}")

    logging.info("DB has been succesfully sent")


async def setTask():
    logging.info("Task has been scheduled")
    schedule.every().day.at("16:50").do(BackUp)
    while 1:
        schedule.run_pending()
        await asyncio.sleep(1)
    
