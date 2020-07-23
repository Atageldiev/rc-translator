#---------------------------------------------------------------------------
#   imports
#---------------------------------------------------------------------------
import asyncio
import schedule
import telebot
import logging 

from datetime import datetime
from aiogram import executor

from loader import translator
from data.config import BACK_UP_CHAT, TOKEN, LANGCODES


#---------------------------------------------------------------------------
#   Initialize variables
#---------------------------------------------------------------------------
teleBot = telebot.TeleBot(TOKEN)
    

#---------------------------------------------------------------------------
#   Functions
#---------------------------------------------------------------------------
def get_translation(text, data: dict = {}, dest: str = ""):
    if not dest:
        dest = LANGCODES.get(data["dest"])
        
    return translator.translate(text, dest=dest).text


def BackUp():                                                               # back up db and log files
    with open("data/server.db", "rb") as dbFile, open("data/bot.log", "rb") as logFile:
        date = str(datetime.now()).rsplit(".")[0]

        teleBot.send_document(chat_id=BACK_UP_CHAT, data=dbFile, caption=f"База данных на {date}")
        teleBot.send_document(chat_id=BACK_UP_CHAT, data=logFile, caption=f"Логи на {date}")

        logging.info("Back up finished successfully")

async def setTask():                                                        # scheduler
    logging.info("Task has been scheduled")
    schedule.every().day.at("19:55").do(BackUp)
    while 1:
        schedule.run_pending()
        await asyncio.sleep(1)
    
