from abc import ABC

from .base import BaseHandler


class MessageHandler(BaseHandler, ABC):
    def message_filter(self, message) -> bool or str:
        return "__all__"

    def _message_filters(self):
        if self.message_filter == "__all__":
            return []
        return [self.message_filter] if not isinstance(self.message_filter, list) else self.message_filter

    def __init_subclass__(cls, **kwargs):
        MessageHandler._make_classmethod(cls, "message_filter")
        super().__init_subclass__(**kwargs)
