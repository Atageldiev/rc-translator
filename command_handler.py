# import from aoiogram
from aiogram import types

# import from my files
from loader import dp, db
from config import ADMIN_ID, LANGS, ALLOWED_LANGS
from myclass import Parser
from mymodule import answer_by_chat_id
from utils import WordStates, AdminStates

async def command_start(message):
    db.user_id_exists(user_id=message.from_user.id, name=message.from_user.first_name)

    await message.reply("Привет, это бот для поиска переводов для различных слов\n/translate")

async def command_translate(message):
    db.user_id_exists(user_id=message.from_user.id, name=message.from_user.first_name)

    state = dp.current_state(user=message.from_user.id)

    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=3, one_time_keyboard=True)
    for element in LANGS:
        markup.insert(types.KeyboardButton(text=element))

    await message.answer("Выберите язык <b><u>с которого</u></b> хотите перевести", reply_markup=markup)
    await state.set_state(WordStates.all()[0])

async def admin_command_users(message):
    users = []
    for el in db.get_user_ids():
        user_id = el[0]
        users.append(user_id)
    await answer_by_chat_id(chat_id=ADMIN_ID, text=f"Батя, бот ща насчитывает:---   <b>{len(users)}</b>   ---пользователей")

async def admin_command_send_all(message):
    state = dp.current_state(user=message.from_user.id)
    await message.answer("Бать, напиши сообщение, которое хочешь отправить всем юзерам")

    await state.set_state(AdminStates.all()[0])



async def state_choose_lang_into(message):
    lang_from = message.text 
    db.update_value(name="lang_from", value=lang_from, user_id=message.from_user.id)

    state = dp.current_state(user=message.from_user.id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True)
    for element in ALLOWED_LANGS.get(lang_from):
        markup.insert(types.KeyboardButton(text=element))
           
    await message.answer("Выберите язык <b><u>на который</u></b> хотите перевести", reply_markup=markup)
    await state.set_state(WordStates.all()[1])

async def state_send_word(message):
    db.update_value(name="lang_into", value=message.text, user_id=message.from_user.id)

    state = dp.current_state(user=message.from_user.id)

    markup = types.ReplyKeyboardMarkup()

    
    await message.answer("Напишите слово, которое хотите перевести", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(WordStates.all()[2])

async def state_send_result(message):
    state = dp.current_state(user=message.from_user.id)
    word = message.text 
    lang_from = db.get_value(name="lang_from", user_id=message.from_user.id)
    lang_into = db.get_value(name="lang_into", user_id=message.from_user.id)

    db.update_value(name="word", value=word, user_id=message.from_user.id)
    await Parser.parse(message, word, lang_from, lang_into, state=1)
    await state.reset_state()

async def admin_state_send_message_all(message):
    for el in db.get_user_ids():
        user_id = el[0]
        await answer_by_chat_id(chat_id=user_id, text=message.text)

    await answer_by_chat_id(chat_id=ADMIN_ID, text="Бать, я закончил")
    await state.reset_state()
