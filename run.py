from aiogram import Dispatcher, executor, types
from aiogram.utils.executor import start_webhook
from loguru import logger
from support import logger_conf

DEBUG_LOGGING = True  # Enable\Disable logging of all messages
DEBUG_ALL = False  # Enable\Disable logging all, include chat messages
logger_conf.start(DEBUG_LOGGING)

import config as cfg
from support.bots import dp, bot
from support.middleware import LoguruMiddleware
import plugins
import utils

if DEBUG_LOGGING and DEBUG_ALL:
    dp.middleware.setup(LoguruMiddleware())


@dp.errors_handler()
async def errors(update: types.Update, error: Exception):
    logger.warning(update)
    try:
        raise error
    except Exception as e:
        logger.exception(e)
    return True


async def on_startup(dsp: Dispatcher):
    bot_info = await dsp.bot.me

    await plugins.initialize_plugins()
    await utils.initialize_utils()

    logger.info(f"Bot {bot_info.full_name} [@{bot_info.username}] started!")


async def on_shutdown(dsp: Dispatcher):
    logger.warning("Shutting down...")

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dsp.storage.close()
    await dsp.storage.wait_closed()

    logger.info("Bye bye!")


if __name__ == "__main__":
    if cfg.POLLING == "True":
        logger.info("Connection type - POLLING")
        executor.start_polling(
            dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True
        )
    else:
        logger.info("Connection type - WEBHOOK")
        start_webhook(
            dispatcher=dp,
            webhook_path=cfg.WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=cfg.WEBAPP_HOST,
            port=cfg.WEBAPP_PORT,
        )
