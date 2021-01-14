from aiogram.types import ChatActions


def typing_action(fn):
    async def wrapper(message):
        await ChatActions.typing()
        return await fn(message)

    return wrapper
