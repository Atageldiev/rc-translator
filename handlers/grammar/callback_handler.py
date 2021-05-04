from aiogram.types import CallbackQuery

from core.settings import dp
from core.parser import get_ikb_by_parsing_native_english
from utils.formatters import bold
from .utils import load_json_by_filename, get_ikb_by_key_from_json

callbacks: dict = load_json_by_filename("callbacks.json")


def is_parsing_callback(cb_data: str) -> bool:
    buttons_data = callbacks.get(cb_data)
    return isinstance(buttons_data, str) and buttons_data.startswith("https")


@dp.callback_query_handler(lambda call: call.data in callbacks.keys() and is_parsing_callback(call.data))
async def handle_parsing_callbacks(call: CallbackQuery):
    await call.message.answer("Нажмите на соответствующую кнопку, чтобы перейти на сайт и почитать подробнее",
                              reply_markup=get_ikb_by_parsing_native_english(callbacks.get(call.data)))


@dp.callback_query_handler(lambda call: call.data in callbacks.keys() and not is_parsing_callback(call.data))
async def handle_markup_callbacks(call: CallbackQuery):
    await call.message.answer(bold("Найденный материал: "),
                              reply_markup=get_ikb_by_key_from_json(call.data, "callbacks.json"))
