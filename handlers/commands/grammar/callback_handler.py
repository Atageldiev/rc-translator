from aiogram.types import CallbackQuery

from core.conf import dp
from utils.parser import parse_native_english
from .utils import get_json_data, get_markup_by_key_from_json

callbacks: dict = get_json_data("callbacks.json")


@dp.callback_query_handler(lambda call: call.data in callbacks.keys())
async def handle_grammar_callbacks(call: CallbackQuery):
    data = callbacks.get(call.data)
    is_parsing_callback = isinstance(data, str) and data.startswith("https")

    await call.answer("Loading...")
    if is_parsing_callback:
        return await handle_parsing_callbacks(call)

    return await handle_markup_callbacks(call)


async def handle_parsing_callbacks(call: CallbackQuery):
    await parse_native_english(call.message, url=callbacks.get(call.data))


async def handle_markup_callbacks(call: CallbackQuery):
    markup = get_markup_by_key_from_json(call.data)
    await call.message.answer("<b>Найденный материал: </b>", reply_markup=markup)
