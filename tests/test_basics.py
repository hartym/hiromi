from dataclasses import dataclass

from jinja2 import Template

from hiromi.contacts import EmailContact
from hiromi.environment import Environment
from hiromi.handlers import MediumHandler
from hiromi.message import Message


@dataclass
class SentEmailMessage:
    sender: EmailContact
    recipient: EmailContact
    subject: str
    body: str


class EmailHandler(MediumHandler):
    def load(self, message, context):
        return Template("Hello, world. This is " + message.name + " message.")

    def render(self, template: Template, **context):
        return template.render(context)

    def send(self, rendered, recipient: EmailContact, sender: EmailContact):
        return SentEmailMessage(sender=sender, recipient=recipient, subject="", body=rendered)


class EatAtJoeMessage(Message):
    name = "eat_at_joe"


def test_basic_notification():
    notifications = Environment()
    notifications.add_medium_handler("email", EmailHandler())

    message = EatAtJoeMessage()
    context = {"language": "fr"}

    recipient = EmailContact("Romain Dorgueil", "romain@dorgueil.net")
    sender = EmailContact("Makersquad", "noreply@makersquad.fr")

    sent = notifications.send(message, context, recipients=[recipient], sender=sender)

    assert len(sent) == 1

    assert sent[0].sender == sender
    assert sent[0].recipient == recipient
    assert sent[0].body == "Hello, world. This is eat_at_joe message."
