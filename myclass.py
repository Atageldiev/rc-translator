# import from required libraries
from bs4 import BeautifulSoup as BS
import requests
from aiogram import types
import sqlite3
# import from my files


class Parser():
    def __getText(text):
        return " ".join(text.split())

    async def __parse_examples(html, message):
        if html.select('.example') != []:
            msg = "<b>Вот все примеры с этим словом:</b>\n"
            for el in html.select('.example'):
                text1 = el.select('.ltr.src')
                text2 = el.select('.ltr.trg')
                msg += "---" + Parser.__getText(text1[0].text) + "\n"
                msg += "---" + Parser.__getText(text2[0].text) + "\n\n"
        else:
            msg = ("ERROR, TRY AGAIN\n/translate")
        await message.answer(msg)

    async def __parse_translations(html, message):
        if html.select('.translation.ltr') != []: 
            markup = types.InlineKeyboardMarkup(row_width=3, inline_keyboard=True)
            for el in html.select('.translation.ltr'):
                text = Parser.__getText(el.text) + "\n"
                url = "https://context.reverso.net" + str(el.get('href'))
                markup.insert(types.InlineKeyboardButton(text=text, url=url))
            markup.add(types.InlineKeyboardButton(text="Нажмите сюда чтобы показать все примеры", callback_data="show_examples"))
            await message.answer("<b>Вот все переводы этого слова</b>\n<em><u>Нажмите на соответствующую кнопку, чтобы перейти на сайт, чтобы увидеть примеры только с этим словом:</u></em>", reply_markup=markup)
        else:
            await message.answer("ERROR, TRY AGAIN\n/translate")
        

    async def parse(message, word: str, lang_from: str, lang_into: str, state: int):
        URL=f"https://context.reverso.net/перевод/{lang_from}-{lang_into}/" + word
        HEADERS={'user-agent': 'my-app/0.0.1'}

        response = requests.get(URL, headers=HEADERS)
        html = BS(response.content, "html.parser")
        
        if state == 1:
            await Parser.__parse_translations(html, message)
        elif state == 2:
            await Parser.__parse_examples(html, message)


class Sqlighter():
    def __init__(self, database="server.db"):
        self.connection = sqlite3.connect(
            database=database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def create_table(self):
        """Создаст таблицу"""
        with self.connection:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS status(
                user_id INT,
                name STRING,
                word STRING,
                lang_from STRING,
                lang_into STRING,
                words_translated INT
                )""")
    
    def user_id_exists(self, user_id, name):
        """Проверит есть ли такой юзер в базе, если нет - добавит"""
        with self.connection:
            self.cursor.execute(
                f"SELECT user_id FROM status WHERE user_id={user_id}")
            if self.cursor.fetchone() is None:
                self.cursor.execute(
                    f"INSERT INTO status VALUES (?, ?, ?, ?, ?, ?)", (user_id, name, "", "", "", 0))
    
    def get_user_ids(self):
        """Берем все user_id в базе"""
        with self.connection:
            return self.cursor.execute(f"SELECT user_id FROM status").fetchall()

    def get_value(self, name, user_id):
        with self.connection:
            for i in self.cursor.execute(f"SELECT {name} FROM status WHERE user_id = {user_id}"):
                return i[0]
    
    def update_value(self, name, value, user_id):
        with self.connection:
            try:
                self.cursor.execute(
                    f"UPDATE status SET {name}={value} WHERE user_id = {user_id}")
            except:
                self.cursor.execute(f"UPDATE status SET {name}='{value}' WHERE user_id = {user_id}")