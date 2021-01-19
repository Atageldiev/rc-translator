from abc import ABC

from aiogram.dispatcher.filters import Command

from .base import BaseHandler


class CommandHandler(BaseHandler, ABC):
    commands: list[str] = NotImplemented
    _must_be_implemented_attrs = ["commands"]

    def _message_filters(self) -> list:
        return [Command(self.commands)]
