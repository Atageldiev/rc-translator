import logging
import requests

from bs4 import BeautifulSoup as BS

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import HEADERS
# Class for parsing
class Parser():
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

    def parse_examples(self, data, num):
        """Parses only examples from context.reverso.net"""
        html = self.__getHtml(data)
        word = data["word"]

        if html.select('.example'):
            msg = "Вот примеры\n"
            
            html = html.select('.example')[num-2:num+1]
            
            for el in html:
                text1 = el.select('.ltr.src')
                text2 = el.select('.ltr.trg')
                
                msg += "---" + self.__getText(text1[0].text) + "\n"
                msg += "---" + self.__getText(text2[0].text) + "\n\n"
                
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(text="Еще примеры", callback_data="more_examples"))
            return msg, markup
        else:
            return "ERROR, TRY AGAIN", None

    def parse_translations(self, data):
        """
        Parses only translations from context.reverso.net
        Creates buttons and sends them directly to the user:
            Text on buttons - translation of the word
            URL on buttons - link to context.reverso.net where examples that are only with the requested word
            Max number of buttons - 6
        """
        html = self.__getHtml(data)
        word = data["word"]
        msg = f"Вот переводы слова {word}\nНажмите на соответствующую кнопку, чтобы перейти на сайт и увидеть примеры только с этим словом:"
        
        if html.select('.translation.ltr'):
            markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=True)

            for el in html.select('.translation.ltr')[:6]:
                text = self.__getText(el.text)
                url = "https://context.reverso.net" + str(el.get('href'))

                markup.insert(InlineKeyboardButton(text=text, url=url))

            markup.add(InlineKeyboardButton(text="Показать примеры", callback_data="show_examples"))

            return msg, markup
        else:
            return "ERROR, TRY AGAIN", None

    async def parse_native_english(self, message, url):
        """
        Parses native-english.ru, and gets links to the websites about requested rule of english
        """
        response = requests.get(url, headers=HEADERS)
        html = BS(response.content, "html.parser")

        html = html.select('.list__item > a')
        if html:
            del html[-3:]

            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(
                text="Определение | Definition", url=url))

            for el in html:
                url = "https://www.native-english.ru" + str(el.get('href'))
                text = self.__getText(el.text)

                markup.add(InlineKeyboardButton(text=text, url=url))

            await message.answer("Вот что я нашел:\nНажмите на соответствующую кнопку, чтобы перейти на сайт и почитать подробнее", reply_markup=markup)
        else:
            logging.critical("NATIVE ENGLISH HAS CHANGED ITS ARCHITECTURE")

            await message.answer("FATAL ERROR.\n\nPlease text my father\n\nLink is in my description")
