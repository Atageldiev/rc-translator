from aiogram.types import ChatActions

from core.database import db


def typing_action(fn):
    """Displays 'Typing...' action in messenger when decorated handler is called"""
    async def wrapper(*args, **kwargs):
        await ChatActions.typing()
        return await fn(*args, **kwargs)

    return wrapper


def check_user_existance(fn):
    """Checks if current user exists in DB"""
    async def wrapper(*args, **kwargs):
        db.user_exists()
        return await fn(*args, **kwargs)

    return wrapper
