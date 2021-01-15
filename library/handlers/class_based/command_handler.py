from abc import abstractmethod
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from core.conf import dp


class CommandHandler:
    commands: list[str] = NotImplemented
    decorators = []
    __must_be_implemented_attrs = ["commands"]

    @abstractmethod
    async def handle(self, message: Message):
        raise NotImplementedError("handle() must be implemented!")

    def __init_subclass__(cls, **kwargs):
        CommandHandler.__check_if_implemented(cls)

        cls.handle = classmethod(cls.handle)
        handler_func = cls.handle

        if dp.message_handler in cls.decorators:
            raise RuntimeError("dp.message_handler() mustn't be included in `decorators` attribute")
        for decorator in cls.decorators:
            if not callable(decorator):
                raise ValueError("Decorator must be callable")
            handler_func = decorator(handler_func)

        dp.message_handler(Command(cls.commands))(handler_func)

    @classmethod
    def __check_if_implemented(cls, subclass):
        for attr in cls.__must_be_implemented_attrs:
            if attr == "commands":
                cls.__set_commands_attribute_by_subclassname(subclass)
                continue

            if getattr(subclass, attr) == NotImplemented:
                raise NotImplementedError(f"{attr} attribute must be implemented!")

    @classmethod
    def __set_commands_attribute_by_subclassname(cls, subclass):
        attr_name = "commands"
        prefix_name = "Handler"
        subclassname: str = subclass.__name__

        if getattr(subclass, attr_name) != NotImplemented:
            return

        if subclassname.endswith(prefix_name):
            setattr(subclass, attr_name, subclassname.removesuffix(prefix_name))
        else:
            raise NotImplementedError(f"Implement `{attr_name}` attribute or "
                                      f"add '{prefix_name} prefix to {subclassname}'")
