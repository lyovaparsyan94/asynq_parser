from abc import ABC,  abstractmethod


class BaseHandler(ABC):

    @abstractmethod
    def start(self):
        ...
