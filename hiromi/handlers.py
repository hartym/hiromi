from abc import ABCMeta, abstractmethod


class MediumHandler(metaclass=ABCMeta):
    @abstractmethod
    def load(self, message, context):
        raise NotImplementedError("No loader implemented.")

    @abstractmethod
    def render(self, template, **context):
        raise NotImplementedError("No renderer implemented.")

    @abstractmethod
    def send(self, rendered, recipient, sender):
        raise NotImplementedError("No sender implemented.")
