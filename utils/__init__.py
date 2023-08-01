from utils import media_sync
from loguru import logger
from aiogram import md, types


async def initialize_utils():
    await media_sync.on_startup()
    # Here you can add another utils

    logger.trace("utils loaded")
