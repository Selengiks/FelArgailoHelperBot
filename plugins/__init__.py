from imports.global_imports import *
from imports.env_import import *
from plugins.channel import followers
from plugins.channel.notifier import stream_notifier
from plugins.chat.stealer import stealer, leaderboard
from plugins.chat.unpinner import unpin


async def initialize_plugins():
    # await followers.on_startup()
    # await stream_notifier.on_startup()
    await stealer.on_startup()
    await leaderboard.on_startup()
    await unpin.on_startup()
    # Here you can add another plugins

    logger.trace("plugins loaded")
