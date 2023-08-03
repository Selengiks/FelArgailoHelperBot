import os
from dotenv import load_dotenv
from loguru import logger
from plugins.channel.notifier import get_twich_notification, get_youtube_notification

load_dotenv()

twitch_integration = True
youtube_integration = True


async def on_startup():
    if twitch_integration:
        await get_twich_notification.on_startup(
            os.getenv("TWITCH_CLIENT_ID"),
            os.getenv("TWITCH_CLIENT_SECRET"),
            os.getenv("TWITCH_USERNAME"),
        )
    if youtube_integration:
        await get_youtube_notification.on_startup()
    if not twitch_integration and youtube_integration:
        logger.warning("No stream platform enabled")

    logger.trace("notifier loaded")
