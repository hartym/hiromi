from abc import ABCMeta, abstractmethod


class MediumHandler(metaclass=ABCMeta):
    @abstractmethod
    def load(self, message, context, **variants):
        raise NotImplementedError("No loader implemented.")

    @abstractmethod
    def render(self, message, template, context):
        raise NotImplementedError("No renderer implemented.")

    @abstractmethod
    def send(self, message, rendered, context):
        raise NotImplementedError("No sender implemented.")
