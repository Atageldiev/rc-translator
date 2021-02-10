from aiogram.dispatcher.filters.state import State, StatesGroup


class Admin(StatesGroup):
    message_one_chat_id = State()
    message_one_text = State()

    send_message_all = State()
