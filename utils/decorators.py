from aiogram.types import ChatActions

from core.database import db


def typing_action(fn):
    async def wrapper(message):
        await ChatActions.typing()
        return await fn(message)

    return wrapper


def check_user_existance(fn):
    async def wrapper(message):
        db.user_exists()
        return await fn(message)

    return wrapper
