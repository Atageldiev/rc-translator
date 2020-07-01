# import from required libraries
from bs4 import BeautifulSoup as BS
import requests
from aiogram import types

# import from my files


class Parser():
    def __getText(text):
        return " ".join(text.split())

    def __parse_examples(html):
        if html.select('.example') != []:
            msg = "<b>Вот все примеры с этим словом:</b>\n"
            for el in html.select('.example'):
                text1 = el.select('.ltr.src')
                text2 = el.select('.ltr.trg')
                msg += "---" + Parser.__getText(text1[0].text) + "\n"
                msg += "---" + Parser.__getText(text2[0].text) + "\n\n"
        else:
            msg = ("ERROR, TRY AGAIN")
        return msg

    def __parse_translations(html):
        if html.select('.translation.ltr') != []:
            msg = "<b>Вот все переводы этого слова</b>\n<em><u>Нажмите на соответствующую кнопку, чтобы перейти на сайт, чтобы увидеть примеры только с этим словом:</u></em>"
            markup = types.InlineKeyboardMarkup(row_width=3, inline_keyboard=True)
            for el in html.select('.translation.ltr'):
                text = Parser.__getText(el.text) + "\n"
                url = "https://context.reverso.net" + str(el.get('href'))
                markup.insert(types.InlineKeyboardButton(text=text, url=url))
        else:
            msg = "ERROR, TRY AGAIN"
        return msg, markup

    async def parse(message, word):
        URL="https://context.reverso.net/перевод/русский-английский/" + word
        HEADERS={'user-agent': 'my-app/0.0.1'}

        response=requests.get(URL, headers=HEADERS)
        html=BS(response.content, "html.parser")
        msg, button = Parser.__parse_translations(html)
        await message.answer(msg, reply_markup=button)
        await message.answer(Parser.__parse_examples(html))
