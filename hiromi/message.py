import inspect
import os
from typing import Dict, Set

from jinja2 import Template


class Message:
    name: str = None
    media: Set[str] = None
    schema: Dict = None

    # Placeholders for message send lifecycle
    template = None
    rendered = None

    def validate(self, parameters):
        return parameters

    default_templates = {}

    def get_default_template(self, medium, *variant):
        if medium not in self.default_templates:
            self.default_templates[medium] = {}

        if variant not in self.default_templates[medium]:
            filename = ".".join(
                (
                    os.path.join(os.path.dirname(inspect.getfile(type(self))), "templates", self.name),
                    medium,
                    *variant,
                    "j2",
                )
            )
            with open(filename) as f:
                self.default_templates[medium][variant] = Template(f.read())

        return self.default_templates[medium][variant]


class Envelope:
    message = None

    def __init__(self, message: Message):
        self.message = message
