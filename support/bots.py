from imports.global_imports import *
from aiogram.bot.api import TELEGRAM_PRODUCTION, TelegramAPIServer
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config as cfg

local_server = TELEGRAM_PRODUCTION
if cfg.LOCAL_SERVER_URL:
    local_server = TelegramAPIServer.from_base(cfg.LOCAL_SERVER_URL)
bot = Bot(
    token=cfg.BOT_TOKEN, validate_token=True, parse_mode="HTML", server=local_server
)
dp = Dispatcher(bot, storage=MemoryStorage())
