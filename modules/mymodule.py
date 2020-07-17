# import from required libraries
import asyncio
import schedule
import telebot
import logging 

from datetime import datetime
from aiogram import executor

# import from my files
from data.config import backUpChat, TOKEN

teleBot = telebot.TeleBot(TOKEN)
    
def BackUp():
    with open("data/server.db", "rb") as dbFile, open("mylog.log", "rb") as logFile:
        date = str(datetime.now()).rsplit(".")[0]

        teleBot.send_document(chat_id=backUpChat, data=dbFile, caption=f"База данных на {date}")
        teleBot.send_document(chat_id=backUpChat, data=logFile, caption=f"Логи на {date}")

        logging.info("Back up finished successfully")

async def setTask():
    logging.info("Task has been scheduled")
    schedule.every().day.at("19:55").do(BackUp)
    while 1:
        schedule.run_pending()
        await asyncio.sleep(1)
    
