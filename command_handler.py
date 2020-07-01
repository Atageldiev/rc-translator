# import from my files
from loader import dp
from config import ADMIN_ID
from myclass import Parser
from utils import States

async def send_welcome(message):
    print(message.from_user.id)
    await message.reply("Привет, это бот для поиска переводов для различных слов\n/translate")

async def command_translate(message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(States.all()[0])
    await message.answer("Напишите слово на английском, либо на русском, которое хотели бы перевести")

async def translate_state_0(message):
    state = dp.current_state(user=message.from_user.id)
    await Parser.parse(message, message.text)
    await state.reset_state()

