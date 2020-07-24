import logging
import telebot
import schedule
import asyncio

from loader import parser, learner
from data.config import TOKEN

teleBot = telebot.TeleBot(
    token=TOKEN, 
    skip_pending=True,
    parse_mode="HTML"
    )



def get_word():
    word_id = learner.get_word_id()
    
    with open("words.txt", "r") as words:
        content = words.readlines()
        word = content[word_id].replace("\n", "")
        return word


data = {
    "src": "английский",
    "dest": "русский",
    "word": get_word()
}

def get_translation_example(data):
    translation, tmarkup = parser.parse_translations(data)
    
    if not tmarkup:
        translation = "Что-то пошло не так\n\nНапишите моему бате: @t2elzeth"
        markup = None
    else:
        
        markup = telebot.types.InlineKeyboardMarkup(row_width=3)
        for el in tmarkup["inline_keyboard"][0]:
            el = dict(el)
            markup.add(telebot.types.InlineKeyboardButton(text=el["text"], url=el["url"]))

    example, trash = parser.parse_examples(data, 4)                                             # second variable is called "trash", cause there is no need in it
    if not trash:
        example = "Что-то пошло не так\n\nНапишите моему бате: @t2elzeth"
    return translation, markup, example

def send_learner(subs: list, state=None):
    translation, markup, example = get_translation_example(data)
    word = data["word"]
    
    logging.info("Sending words")
    
    for user_id in subs:
        teleBot.send_message(chat_id=user_id, text=f"<b>Привет</b>🤪💫\n\n\
Наше сегодняшнее слово 💁‍♀️ <em>{word}</em>\n\n\
Нажми 👉 #dailyword 👈, чтобы найти все выученные слова\n\n\
Да прибудет с тобой дух английского💪")
        teleBot.send_message(chat_id=user_id, text=translation, reply_markup=markup)
        teleBot.send_message(chat_id=user_id, text=example)
    if state == "update_word":
        learner.update_word_id()
        logging.info("Word id has been updated")
        
def scheduler():
    subs1 = learner.get_certain_mode_subs(1)
    subs2 = learner.get_certain_mode_subs(2)
    
    schedule.every().day.at("04:00").do(send_learner, subs=subs1)
    schedule.every().day.at("09:00").do(send_learner, subs=subs1)
    schedule.every().day.at("14:00").do(send_learner, subs=subs1, state="update_word")
    
    schedule.every().day.at("05:00").do(send_learner, subs=subs2, state="update_word")
    schedule.every().day.at("09:00").do(send_learner, subs=subs2, state="update_word")
    schedule.every().day.at("13:00").do(send_learner, subs=subs2)
    
    
    
    logging.info("All tasks have been scheduled")
    
    


