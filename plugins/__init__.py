from plugins.channel import followers
from loguru import logger


async def initialize_plugins():
    await followers.on_startup()
    # Here you can add another plugins

    logger.debug("plugins loaded")
