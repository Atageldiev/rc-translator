from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_ikb(data, row_width=3):
    """Rerturns InlineKeyboardMarkup, that's ready to use in message"""
    markup = InlineKeyboardMarkup(row_width=row_width)
    for button_data in data:
        markup.insert(InlineKeyboardButton(**button_data))
    return markup
