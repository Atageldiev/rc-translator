from aiogram.dispatcher.filters.state import State, StatesGroup

class WordStates(StatesGroup):
    num = 3

    lang_from = State()
    lang_into = State()
    word = State()
    res = State()
    

class AdminStates(StatesGroup):

    message_one_chat_id = State()
    message_one_text = State()

    send_message_all = State()
    setDB = State()
    

class LearningMode(StatesGroup):
    
    mode = State()
