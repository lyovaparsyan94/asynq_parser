import asyncio

from handlers.manager import Manager
from handlers.config_loader import ConfigLoader
from config.constants import (
    CONFIG_FILE,
)


async def main():
    config = ConfigLoader.load_config(file=CONFIG_FILE)
    manager = Manager(config=config)
    await manager.start()


if __name__ == '__main__':
    asyncio.run(main())
