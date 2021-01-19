import json
import os

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as IKB

from core.conf import BASE_DIR

JSONS_DIR = os.path.join(BASE_DIR, "handlers/commands/grammar")


def get_json_data(filename):
    with open(os.path.join(JSONS_DIR, filename)) as f:
        return json.load(f)


async def get_markup_by_key_from_json(key: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=3)
    callbacks: dict = get_json_data("callbacks.json")

    for markup_data in callbacks.get(key):
        markup.insert(IKB(**markup_data))
    return markup
