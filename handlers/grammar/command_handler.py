import json
import os

from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import Message

from core.commands.common import COMMAND_GRAMMAR
from core.database import db
from core.parser import get_ikb_by_parsing_native_english
from core.settings import dp
from utils.buttons import get_ikb
from utils.text import FormattedText
from utils.path import get_current_dir

JSONS_DIR = get_current_dir(__file__)


def load_json_by_filename(filename: str, fileroot=JSONS_DIR) -> dict:
    with open(os.path.join(fileroot, filename)) as f:
        return json.load(f)


def get_ikb_by_key_from_json(key: str, filename, fileroot=JSONS_DIR) -> InlineKeyboardMarkup:
    markup_data: list = load_json_by_filename(filename, fileroot).get(key)
    return get_ikb(markup_data)


callbacks: dict = load_json_by_filename("callbacks.json")


def is_parsing_callback(cb_data: str) -> bool:
    buttons_data = callbacks.get(cb_data)
    return isinstance(buttons_data, str) and buttons_data.startswith("https")


@dp.message_handler(Command(COMMAND_GRAMMAR))
async def handle_grammar(message: Message):
    db.grammar_used += 1
    await message.answer("Выберите насчет чего вы хотите получить готовую информацию: ",
                         reply_markup=get_ikb_by_key_from_json("default", "callbacks.json"))


@dp.callback_query_handler(lambda call: call.data in callbacks.keys() and is_parsing_callback(call.data))
async def handle_parsing_callbacks(call: CallbackQuery):
    await call.message.answer("Нажмите на соответствующую кнопку, чтобы перейти на сайт и почитать подробнее",
                              reply_markup=get_ikb_by_parsing_native_english(callbacks.get(call.data)))


@dp.callback_query_handler(lambda call: call.data in callbacks.keys() and not is_parsing_callback(call.data))
async def handle_markup_callbacks(call: CallbackQuery):
    await call.message.answer(FormattedText("Найденный материал: ").bold(),
                              reply_markup=get_ikb_by_key_from_json(call.data, "callbacks.json"))
