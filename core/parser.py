import requests
from aiogram.types import User
from bs4 import BeautifulSoup

from core.conf.settings import storage
from utils.buttons import get_ikb
from utils.formatters import strip_text

HEADERS = {'user-agent': 'my-app/0.0.1'}


def get_html(url) -> BeautifulSoup:
    response = requests.get(url, headers=HEADERS)
    return BeautifulSoup(response.content, "html.parser")


def get_current_user():
    """Returns current user instance"""
    return User().get_current()


async def get_current_user_data():
    """Returns data from storage that belongs to current user"""
    return await storage.get_data(user=get_current_user().id)


async def get_message_after_parsing_examples(html, num: int) -> str:
    html = html[num - 2:num + 1]
    msg = "Вот примеры\n"
    for el in html:
        msg += "---" + strip_text(el.select('.src')[0].text) + "\n"
        msg += "---" + strip_text(el.select('.trg')[0].text) + "\n\n"
    return msg


async def get_message_text_by_parsing_examples():
    """Parses only examples from context.reverso.net"""
    data = await get_current_user_data()
    html = get_html(f"https://context.reverso.net/перевод/{data['src']}-{data['dest']}/{data['word']}") \
        .select(".example")
    return await get_message_after_parsing_examples(html, data["examples_number"]) if html else "ERROR, TRY AGAIN"


def get_native_english_url(url) -> str:
    return f"https://www.native-english.ru{url}"


def get_ikb_by_parsing_native_english(url):
    """Parses native-english.ru, and gets links to the websites about requested rule of english"""
    html = get_html(url).select('.list__item > a')[:-3]
    ikb_data = [{"text": strip_text(el.text), "url": get_native_english_url(el.get("href"))} for el in html]
    return get_ikb(ikb_data) if html else None
