#---------------------------------------------------------------------------
#   imports
#---------------------------------------------------------------------------
import logging
import requests
import sqlite3

from bs4 import BeautifulSoup as BS
from aiogram import types

from data.config import HEADERS

# Class to work with database
class Database():
    """
    This class is created to work with DB
    """
    def __init__(self, database="data/server.db"):
        self.connection = sqlite3.connect(
            database=database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def create_table_status(self):
        """Create table `status`"""
        with self.connection:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS status(
                user_id INT,
                name STRING,
                words_translated INT,
                grammar_used INT,
                subbed BOOL,
                learning_mode
                )""")

    def user_id_exists(self, user_id, name):
        """Checks if the user is already in DB, adds if he is not"""
        with self.connection:
            self.cursor.execute(f"SELECT user_id FROM status WHERE user_id={user_id}")
            if self.cursor.fetchone() is None:
                self.cursor.execute(f"INSERT INTO status VALUES (?, ?, ?, ?, ?, ?)", (user_id, name, 0, 0, False, 1))
    
    def get_user_ids(self):
        """Get list of all `user_ids` in DB"""
        with self.connection:
            return self.cursor.execute(f"SELECT user_id FROM status").fetchall()

    def get_value(self, name, user_id):
        """Get value from DB"""
        with self.connection:
            for i in self.cursor.execute(f"SELECT {name} FROM status WHERE user_id = {user_id}"):
                return i[0]
    
    def get_subscribers(self):
        """Get list of subs, whose status `sub` is True"""
        with self.connection:
            return self.cursor.execute(f"SELECT user_id FROM status WHERE sub = True").fetchall()

    def update_value(self, name, value, user_id):
        """Update some value in DB"""
        with self.connection:
            try:
                self.cursor.execute(
                    f"UPDATE status SET {name}={value} WHERE user_id = {user_id}")
            except:
                self.cursor.execute(f"UPDATE status SET {name}='{value}' WHERE user_id = {user_id}")

# Class for parsing
class Parser():
    def __init__(self):
        pass

    def __getText(self, text):
        """Returns a text without any extra spaces anywhere"""
        return " ".join(text.split())
    
    def __getHtml(self, data):
        src = data["src"]
        dest = data["dest"]
        word = data["word"]

        URL = f"https://context.reverso.net/перевод/{src}-{dest}/{word}"
        response = requests.get(URL, headers=HEADERS)
        html = BS(response.content, "html.parser")
        return html

    async def __parse_examples(self, html, message, num):
        """Parses only examples from context.reverso.net"""
        if html.select('.example') != []:
            msg = "<b>Вот примеры с этим словом:</b>\n"
            html = html.select('.example')[num-3:num+1]
            for el in html:
                text1 = el.select('.ltr.src')
                text2 = el.select('.ltr.trg')
                msg += "---" + self.__getText(text1[0].text) + "\n"
                msg += "---" + self.__getText(text2[0].text) + "\n\n"
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text="Еще примеры", callback_data="show_examples"))
            if msg != "<b>Вот примеры с этим словом:</b>\n":
                await message.answer(msg, reply_markup=markup)
            else:
                await message.edit_text("Уже показаны все примеры", reply_markup=None)
        else:
            await message.answer("ERROR, TRY AGAIN\n/translate")

    async def __parse_translations(self, html, message):
        """
        Parses only translations from context.reverso.net
        Creates buttons and sends them directly to the user:
            Text on buttons - translation of the word
            URL on buttons - link to context.reverso.net where examples that are only with the requested word
            Max number of buttons - 6
        """
        if html.select('.translation.ltr') != []:
            markup = types.InlineKeyboardMarkup(row_width=3, inline_keyboard=True)
            for el in html.select('.translation.ltr')[:6]:
                text = self.__getText(el.text)
                url = "https://context.reverso.net" + str(el.get('href'))
                markup.insert(types.InlineKeyboardButton(text=text, url=url))
            markup.add(types.InlineKeyboardButton(text="Показать примеры", callback_data="show_examples"))
            await message.answer("<b>Вот все переводы этого слова</b>\n<em><u>Нажмите на соответствующую кнопку, чтобы перейти на сайт, чтобы увидеть примеры только с этим словом:</u></em>", reply_markup=markup)
        else:
            await message.answer("ERROR, TRY AGAIN\n/translate")

    async def parse_native_english(self, message, url):
        """
        Parses native-english.ru, and gets links to the websites about requested rule of english
        """
        response = requests.get(url, headers=HEADERS)
        html = BS(response.content, "html.parser")

        html = html.select('.list__item > a')
        if html != []:
            del html[-3:]
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(
                text="Определение | Definition", url=url))
            for el in html:
                url = "https://www.native-english.ru" + str(el.get('href'))
                text = self.__getText(el.text)
                markup.add(types.InlineKeyboardButton(text=text, url=url))
            await message.answer("<b>Вот что я нашел: </b>\n<em>Нажмите на соответствующую кнопку, чтобы перейти на сайт и почитать подробнее</em>", reply_markup=markup)
        else:
            logging.critical("NATIVE ENGLISH HAS CHANGED ITS ARCHITECTURE")
            await message.answer("FATAL ERROR.\n\nPlease text my father\n\nLink is in my description")
    
    async def parse_sentence(self, message, text):
        URL = f"https://translate.google.com/#view=home&op=translate&sl=en&tl=ru&text={text}"
        response = requests.get(URL, headers=HEADERS)
        html = BS(response.content, "html.parser")
        html = html.select(".tlid-translation.translation > span")
        print(html)

    async def parse(self, message, data, level=1, num=3):
        """
        Parent function that calls functions __parse_translations() and __parse_examples
        according to given `level` argument
        """
    
        if level==1:
            html = self.__getHtml(data)
            await self.__parse_translations(html, message) 
            
        elif level==2:
            html = self.__getHtml(data)
            await self.__parse_examples(html, message, num)
            
