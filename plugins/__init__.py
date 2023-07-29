from plugins.channel import followers
from plugins.chat import stealer
from loguru import logger


async def initialize_plugins():
    await followers.on_startup()
    await stealer.on_startup()
    # Here you can add another plugins

    logger.debug("plugins loaded")
