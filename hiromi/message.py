from typing import Dict, Set


class Message:
    name: str = None
    media: Set[str] = None
    schema: Dict = None

    # Placeholders for message send lifecycle
    template = None
    rendered = None

    def validate(self, parameters):
        return parameters


class Envelope:
    message = None

    def __init__(self, message: Message):
        self.message = message
