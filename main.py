import logging
import hannnndlers

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

from data.config import TOKEN

logging.basicConfig(level=logging.INFO)


from loader import dp



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
