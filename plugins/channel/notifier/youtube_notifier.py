from loguru import logger


async def on_startup():
    logger.trace("youtube_notifier loaded")
