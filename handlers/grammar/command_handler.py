from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from core.conf.settings import dp
from core.commands.common import COMMAND_GRAMMAR
from core.database import db
from .utils import get_ikb_by_key_from_json


@dp.message_handler(Command(COMMAND_GRAMMAR))
async def handle_grammar(message: Message):
    db.grammar_used += 1
    await message.answer("Выберите насчет чего вы хотите получить готовую информацию: ",
                         reply_markup=get_ikb_by_key_from_json("default", "callbacks.json"))
