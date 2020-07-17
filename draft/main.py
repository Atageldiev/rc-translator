import threading
import time
import schedule
import asyncio
# import from aiogram
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# import from custom files
from data.config import TOKEN
from classes.myclass import Sqlighter


def dbBackUp():
    print("I AM WORKING...")


async def setTask():
    schedule.every(3).seconds.do(dbBackUp)
    while 1:
        schedule.run_pending()
        await asyncio.sleep(1)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())
    
@dp.message_handler(commands="test")
async def send_welcome(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Najmi", callback_data="n"))
    markup.add(types.InlineKeyboardButton(text="Najmi2", callback_data="n"))
    await message.answer("Privet", reply_markup=markup)

@dp.message_handler(content_types="document")
async def process_empty_msg(message: types.Message):
    print(message.document)
    info = await bot.get_file(message.document.file_id)
    print(info)
    await bot.download_file(file_path=info.file_path, destination="server.db")

@dp.message_handler()
async def process_empty_message(message: types.Message):
    print(message.chat.id)


@dp.callback_query_handler(lambda c: c.data == "n")
async def process_n(callback_query: types.CallbackQuery):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton("Privet"))
    await callback_query.message.answer("Privet", reply_markup=markup)

if __name__ == '__main__':
    dp.loop.create_task(setTask())
    executor.start_polling(dp, skip_updates=True)
