from abc import ABC, abstractmethod


class BaseConfigLoader(ABC):

    @staticmethod
    @abstractmethod
    def load_config(file):
        ...
