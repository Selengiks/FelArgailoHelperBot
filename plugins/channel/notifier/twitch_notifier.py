from loguru import logger


async def on_startup(client_id, client_secret):
    logger.trace("twitch_notifier loaded")
