import requests
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bs4 import BeautifulSoup

from utils.buttons import get_ikb

HEADERS = {'user-agent': 'my-app/0.0.1'}


def __get_text(text: str) -> str:
    """Returns a text without any extra spaces anywhere"""
    return " ".join(text.split())


def __get_html(data: dict) -> BeautifulSoup:
    url = f"https://context.reverso.net/перевод/{data['src']}-{data['dest']}/{data['word']}"
    response = requests.get(url, headers=HEADERS)
    return BeautifulSoup(response.content, "html.parser")


def parse_examples(data, num):
    """Parses only examples from context.reverso.net"""
    html = __get_html(data).select(".example")
    if html:
        html = html[num - 2:num + 1]
        msg = "Вот примеры\n"
        for el in html:
            msg += "---" + __get_text(el.select('.src')[0].text) + "\n"
            msg += "---" + __get_text(el.select('.trg')[0].text) + "\n\n"
        return msg, get_ikb({"text": "Еще примеры", "callback_data": "more_examples"})
    else:
        return "ERROR, TRY AGAIN", None


async def parse_native_english(message, url):
    """Parses native-english.ru, and gets links to the websites about requested rule of english"""
    response = requests.get(url, headers=HEADERS)
    html = BeautifulSoup(response.content, "html.parser").select('.list__item > a')[:-3]
    if html:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Определение | Definition", url=url))

        for el in html:
            url = "https://www.native-english.ru" + str(el.get('href'))
            markup.add(InlineKeyboardButton(text=__get_text(el.text), url=url))

        await message.answer(
            "Вот что я нашел:\nНажмите на соответствующую кнопку, чтобы перейти на сайт и почитать подробнее",
            reply_markup=markup)
    else:
        await message.answer("FATAL ERROR.\n\nPlease text my father\n\nLink is in my description")
