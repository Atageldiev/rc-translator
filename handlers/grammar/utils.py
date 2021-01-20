import json
import os

from aiogram.types import InlineKeyboardMarkup

from utils.buttons import get_ikb
from utils.path import get_current_dir

JSONS_DIR = get_current_dir(__file__)


def load_json_by_filename(filename: str, fileroot=JSONS_DIR) -> dict:
    with open(os.path.join(fileroot, filename)) as f:
        return json.load(f)


def get_ikb_by_key_from_json(key: str, filename, fileroot=JSONS_DIR) -> InlineKeyboardMarkup:
    markup_data: list = load_json_by_filename(filename, fileroot).get(key)
    return get_ikb(markup_data)
