import telebot
from config import TOKEN, saveDB
from datetime import datetime

bot = telebot.TeleBot(TOKEN)

def backUpDB():
    with open("server.db", "rb") as fileDB:
        bot.send_document(chat_id=saveDB, data=fileDB, caption=f"База данных на {datetime.now()}")
