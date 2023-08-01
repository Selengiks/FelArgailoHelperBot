import os
from dotenv import load_dotenv
from loguru import logger
from plugins.channel.notifier import twitch_notifier, youtube_notifier

load_dotenv()

twitch_integration = True
youtube_integration = True


async def on_startup():
    if twitch_integration:
        await twitch_notifier.on_startup(
            os.getenv("TWITCH_CLIENT_ID"), os.getenv("TWITCH_CLIENT_SECRET")
        )
    if youtube_integration:
        await youtube_notifier.on_startup()
    if not twitch_integration and youtube_integration:
        logger.warning("No stream platform enabled")

    logger.trace("notifier loaded")
