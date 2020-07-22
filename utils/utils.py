from aiogram.dispatcher.filters.state import State, StatesGroup

class Word(StatesGroup):
    num = 3

    src = State()
    dest = State()
    word = State()
    res = State()
    
class Sentence(StatesGroup):
    src = State()
    dest = State()
    sentence = State()
    res = State()

class Admin(StatesGroup):

    message_one_chat_id = State()
    message_one_text = State()

    send_message_all = State()
    setDB = State()
    
class LearningMode(StatesGroup):
    
    mode = State()
