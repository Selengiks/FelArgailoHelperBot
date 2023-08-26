from imports.global_imports import *
from imports.env_import import *
from aiogram import md

from utils import media_sync


async def initialize_utils():
    await media_sync.on_startup()
    # Here you can add another utils

    logger.trace("utils loaded")
