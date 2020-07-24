import datetime
from typing import Dict, Sequence, Type

from .handlers import MediumHandler
from .message import Message


class Environment:
    handlers: Dict[str, MediumHandler] = None
    languages: Dict[str, str] = None
    listeners: list = None
    default_language: str = None
    messages: Dict[str, Type[Message]] = {}

    def __init__(self, *, default_language=None):
        self.handlers = self.handlers or {}
        self.languages = self.languages or {}
        self.default_language = self.default_language or default_language

    @property
    def media(self) -> set:
        return set(self.handlers.keys())

    def add_medium_handler(self, name, handler):
        self.handlers[name] = handler

    def get_medium_handler(self, name) -> MediumHandler:
        return self.handlers[name]

    def add_language(self, code, name):
        self.languages[code] = name

    def add_message(self, message: Type[Message]):
        self.messages[message.name] = message

    def add_listener(self, listener):
        self.listeners.append(listener)

    def send(self, message, context: Dict, *, recipients, sender):
        if not isinstance(recipients, Sequence):
            recipients = [recipients]

        sent = []

        for medium in self.handlers:
            handler = self.get_medium_handler(medium)
            template = handler.load(message, context)

            for recipient in recipients:
                sent.append(
                    handler.send(
                        handler.render(template, **context, recipient=recipient, sender=sender), recipient, sender,
                    )
                )
        return sent

    def send_later(self, message, context, send_at):
        pass

    def send_soon(self, message, context):
        return self.send_later(message, context, datetime.datetime.now())

    def create(self, name, *args, **kwargs):
        return self.messages[name](*args, **kwargs)
