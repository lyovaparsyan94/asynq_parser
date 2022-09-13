from os.path import (
    abspath,
    dirname,
    join
)

ROOT_DIR = abspath(dirname(__file__))
CONFIG_FILE = join(ROOT_DIR, 'config.yaml')
LOGGER_CONFIG = join(ROOT_DIR, 'logger.yaml')
