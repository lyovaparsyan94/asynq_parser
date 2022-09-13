import yaml
from core.config_loader import BaseConfigLoader


class ConfigLoader(BaseConfigLoader):

    @staticmethod
    def load_config(file):
        with open(file) as stream:
            config = yaml.safe_load(stream=stream)
        return config
