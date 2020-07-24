from typing import Type

from .message import Message


class NotificationTypeRegistry:
    types: dict

    def __init__(self):
        self.types = {}

    def __getitem__(self, item) -> Type[Message]:
        return self.types[item]

    def add(self, notification_type: Type[Message]):
        if notification_type.name in self.types:
            raise ValueError('Notification type "{}" is already defined for this registry')
        self.types[notification_type.name] = notification_type

    def create(self, name):
        return self[name]()
