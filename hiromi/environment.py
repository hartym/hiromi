import datetime
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Sequence

from .handlers import MediumHandler
from .message import Message

logger = logging.getLogger(__name__)


@dataclass
class SentMessage:
    rendered: Dict
    context: Dict
    status: Dict


class Environment:
    handlers: Dict[str, MediumHandler] = None
    languages: Dict[str, str] = None
    default_language: str = None

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

    def on_send(self, message: Message, context: Dict, *, recipients, sender):
        pass

    def on_sent(self, message: Message, context: Dict, results: List[SentMessage]):
        pass

    def send(self, message: Message, context: Dict, *, recipients, sender, language=None):
        if not isinstance(recipients, List):
            recipients = [recipients]

        sent = []
        language = language or self.default_language
        context["language"] = language
        context["media"] = list(set(self.handlers.keys()).intersection(set(message.media)))

        # Allow to extend the before-send behaviour.
        more_context = self.on_send(message, context, recipients=recipients, sender=sender)
        if more_context:
            context.update(more_context)

        for medium in context["media"]:
            handler = self.get_medium_handler(medium)
            templates = {}

            for recipient in recipients:
                # We need a local context copy we can modify.
                current_context = dict(context)
                current_context["medium"] = medium

                # Load the template(s) for the current variant if we did not load it yet.
                if not language in templates:
                    templates[language] = handler.load(message, current_context, language=language)

                # Allow the template loader to extend our context, for example to include database object we want to
                # use later for logging or whatever.
                if templates[language].get("context"):
                    current_context.update(templates[language].get("context"))

                # Add sender and recipient to context.
                current_context["recipient"] = recipient
                current_context["sender"] = sender

                # Render the template(s) using the current sending context.
                rendered = handler.render(message, templates[language], current_context)

                # Send the message
                status = handler.send(message, rendered, current_context)
                logger.info('Sent message "%s" to "%s": %r', message.name, current_context["recipient"], status)

                # Store result for further processing.
                sent.append(SentMessage(rendered, current_context, status))

        # Allow to react after sending is complete.
        self.on_sent(message, context, sent)

        return sent

    def send_later(self, message, context, send_at):
        pass

    def send_soon(self, message, context):
        return self.send_later(message, context, datetime.datetime.now())
