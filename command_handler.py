# import from aoiogram
from aiogram import types

# import from my files
from loader import dp, db, Parser
from config import ADMIN_ID, LANGS, ALLOWED_LANGS, LEARNING_MODE
from mymodule import answer_by_chat_id, saveDoc
from utils import WordStates, AdminStates

async def command_start(message):
    db.user_id_exists(user_id=message.from_user.id, name=message.from_user.first_name)

    await message.reply("Привет, это бот для поиска переводов для различных слов\n/translate")

async def command_translate(message):
    db.user_id_exists(user_id=message.from_user.id, name=message.from_user.first_name)

    state = dp.current_state(user=message.from_user.id)

    db.update_value(name="num", value=3, user_id=message.from_user.id)

    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=3, one_time_keyboard=True)
    for element in LANGS:
        markup.insert(types.KeyboardButton(text=element))

    await message.answer("Выберите язык <b><u>с которого</u></b> хотите перевести", reply_markup=markup)
    await state.set_state(WordStates.all()[0])

async def command_grammar(message):
    db.user_id_exists(user_id=message.from_user.id, name=message.from_user.first_name)
    grammar_used = db.get_value(name="grammar_used", user_id=message.from_user.id)
    db.update_value(name="grammar_used", value=grammar_used + 1, user_id=message.from_user.id)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Глагол | Verb", callback_data="verb"))
    markup.add(types.InlineKeyboardButton(text="Артикли | Articles", callback_data="articles"))
    markup.add(types.InlineKeyboardButton(text="Существительное | Noun", callback_data="noun"))
    markup.add(types.InlineKeyboardButton(text="Прилагательное | Adjective", callback_data="adjective"))
    markup.add(types.InlineKeyboardButton(text="Местоимение | Pronoun", callback_data="pronoun"))
    markup.add(types.InlineKeyboardButton(text="Числительное | Numeral", callback_data="numeral"))
    markup.add(types.InlineKeyboardButton(text="Наречие | Adverb", callback_data="adverb"))
    markup.add(types.InlineKeyboardButton(text="Предлог | Preposition", callback_data="preposition"))
    markup.add(types.InlineKeyboardButton(text="Союз | Conjunction", callback_data="conjunction"))
    markup.add(types.InlineKeyboardButton(text="Частица | Particles", callback_data="particles"))
    markup.add(types.InlineKeyboardButton(text="Междометие | Interjections",url="https://www.native-english.ru/grammar/english-interjections"))
    markup.add(types.InlineKeyboardButton(text="Члены предложения | Parts of a sentence", callback_data="parts"))
    markup.add(types.InlineKeyboardButton(text="Простые предложения | Simple sentences", callback_data="simple_sentences"))
    markup.add(types.InlineKeyboardButton(text="Сложные предложения | Complex sentences", callback_data="complex_sentences"))
    markup.add(types.InlineKeyboardButton(text="Косвенная речь | Indirect speech", callback_data="indirect_speech"))
    markup.add(types.InlineKeyboardButton(text="Пунктуация | Punctuation", url="https://www.native-english.ru/grammar/english-punctuation"))
    await message.answer("Выберите насчет чего вы хотите получить готовую информацию: ", reply_markup=markup)

async def command_rating(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    word = db.get_value(name="word", user_id=user_id)
    words_translated = db.get_value(name="words_translated", user_id=user_id)
    grammar_used = db.get_value(name="grammar_used", user_id=user_id)

    await message.answer(f"<b><u>{name}</u></b>, ваша статистика:\n\
    <em>Слов переведено:</em>- {words_translated}\n \
    <em>Помощника по грамматике использовано:</em>- {grammar_used}\n \
    <em>Последнее переведенное слово:</em>- '{word}'")

async def command_setsub(message):
    db.user_id_exists(user_id=message.from_user.id, name=message.from_user.first_name)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Subscribe/unsubscribe", callback_data="sub_unsub"))
    markup.add(types.InlineKeyboardButton(text="Change learning_mode", callback_data="learning_mode"))


    await message.answer("Что вы хотите сделать?", reply_markup=markup)

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

async def admin_command_setDB(message):
    state = dp.current_state(user=message.from_user.id)

    await message.answer("Отправьте файл, который надо загрузить")
    await state.set_state(AdminStates.all()[1])

async def state_choose_lang_into(message):
    lang_from = message.text 
    if lang_from in LANGS:
        user_id = message.from_user.id
        db.update_value(name="lang_from", value=lang_from, user_id=user_id)

        state = dp.current_state(user=user_id)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True)
        for element in ALLOWED_LANGS.get(lang_from):
            markup.insert(types.KeyboardButton(text=element))
            
        await message.answer("Выберите язык <b><u>на который</u></b> хотите перевести", reply_markup=markup)
        await state.set_state(WordStates.all()[1])
    else:
        await message.answer("ERROR, TRY AGAIN\n/translate", reply_markup=types.ReplyKeyboardRemove())
        await state.reset_state()

async def state_send_word(message):
    user_id = message.from_user.id
    lang_into = message.text
    lang_from = db.get_value("lang_from", user_id)

    if lang_into in ALLOWED_LANGS.get(lang_from):
        db.update_value(name="lang_into", value=lang_into, user_id=user_id)

        state = dp.current_state(user=user_id)
        
        await message.answer("Напишите слово, которое хотите перевести", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(WordStates.all()[2])
    else:
        await message.answer("ERROR, TRY AGAIN\n/translate", reply_markup=types.ReplyKeyboardRemove())
        await state.reset_state()

async def state_send_result(message):
    user_id = message.from_user.id
    state = dp.current_state(user=user_id)
    word = message.text 

    lang_from = db.get_value(name="lang_from", user_id=user_id)
    lang_into = db.get_value(name="lang_into", user_id=user_id)
    words_translated = db.get_value(name="words_translated", user_id=user_id)

    db.update_value(name="words_translated", value=words_translated + 1, user_id=user_id)
    db.update_value(name="word", value=word, user_id=user_id)
    db.update_value(name="num", value=3, user_id=message.from_user.id)

    await Parser.parse(message, word, lang_from, lang_into, state=1)
    await state.reset_state()

async def admin_state_send_message_all(message):
    for el in db.get_user_ids():
        user_id = el[0]
        await answer_by_chat_id(chat_id=user_id, text=message.text)

    await answer_by_chat_id(chat_id=ADMIN_ID, text="Бать, я закончил")
    await state.reset_state()

async def admin_state_setDB(message):
    try:
        document = message.document
        await saveDoc(document)
    except:
        await message.answer("Бать, чет пошло не так")

async def learnerState_0(message):
    user_id = message.from_user.id
    state = dp.current_state(user=user_id)
    
    if message.text == "Mode 1":
        db.update_value("learning_mode", 1, user_id)
        status = 1
        await message.answer(f"Ваш активный режим обучения: <em> {LEARNING_MODE.get(status)}</em>", reply_markup=types.ReplyKeyboardRemove())

    elif message.text == "Mode 2":
        db.update_value("learning_mode", 2, user_id)
        status = 2
        await message.answer(f"Ваш активный режим обучения: <em> {LEARNING_MODE.get(status)}</em>", reply_markup=types.ReplyKeyboardRemove())

    elif message.text == "Mode 3":
        db.update_value("learning_mode", 3, user_id)
        status = 3
        await message.answer(f"Ваш активный режим обучения: <em> {LEARNING_MODE.get(status)}</em>", reply_markup=types.ReplyKeyboardRemove())

    elif message.text == "Cancel":
        await message.answer("Cancelled", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("ERROR, TRY AGAIN\n/setsub", reply_markup=types.ReplyKeyboardRemove())
    await state.reset_state()
