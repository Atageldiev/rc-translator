from abc import abstractmethod

from aiogram.types import Message

from core.conf import dp

INHERITED_HANDLERS = ['CommandHandler', 'MessageHandler']


class BaseHandler:
    decorators: list = []
    _must_be_implemented_attrs: list = []

    @abstractmethod
    async def handle(self, message: Message):
        raise NotImplementedError("handle() must be implemented!")

    @abstractmethod
    def _message_filters(self):
        raise NotImplementedError("message_filters() must be implemented!")

    def __init_subclass__(cls, **kwargs):
        if cls.__name__ in INHERITED_HANDLERS:
            return

        BaseHandler.__check_if_implemented(cls)

        handler_func = BaseHandler._make_classmethod(cls, "handle")
        for decorator in cls.decorators:
            if not callable(decorator):
                raise ValueError("Decorator must be callable")
            handler_func = decorator(handler_func)

        message_filters = BaseHandler._make_classmethod(cls, "_message_filters")
        dp.message_handler(*message_filters())(handler_func)

    @classmethod
    def __check_if_implemented(cls, subclass):
        for attr in getattr(subclass, "_must_be_implemented_attrs"):
            if getattr(subclass, attr) == NotImplemented:
                raise NotImplementedError(f"{attr} attribute must be implemented!")

    @classmethod
    def _make_classmethod(cls, subclass, method_name):
        setattr(subclass, method_name, classmethod(getattr(subclass, method_name)))
        return getattr(subclass, method_name)

    # @classmethod
    # def __make_all_callable(cls, subclass):
    #     for method in [method for method in subclass.__dict__
    #                    if not method.startswith("_")
    #                       and callable(getattr(subclass, method))
    #                       and not inspect.ismethod(getattr(subclass, method))
    #                    ]:
    #         BaseHandler._make_classmethod(subclass, method)
