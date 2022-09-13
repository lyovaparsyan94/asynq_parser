from abc import ABC, abstractmethod


class BaseNotifier(ABC):

    @staticmethod
    @abstractmethod
    def create_message(items):
        ...

    @abstractmethod
    def send(self, homes):
        ...
