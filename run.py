from imports.global_imports import *
import support.logger_conf
import config as cfg
from aiogram.utils import exceptions
from aiogram.utils.executor import start_webhook
from support import dp, bot, tbot, LoguruMiddleware
import plugins
from utils import handler_filters
import utils

DEBUG_LOGGING = (
    "DEBUG"  # [INFO, DEBUG, TRACE] https://loguru.readthedocs.io/en/stable/index.html
)
DEBUG_ALL = False  # Enable\Disable logging all, include chat messages

if DEBUG_LOGGING and DEBUG_ALL:
    dp.middleware.setup(LoguruMiddleware())


@dp.errors_handler()
async def errors(update: types.Update, error: Exception):
    logger.warning(update)
    try:
        raise error
    except exceptions.RetryAfter as e:
        logger.error(
            f"Target [ID:{update.bot.id}]: Flood limit is exceeded. Sleep {e.timeout} seconds."
        )
        await asyncio.sleep(e.timeout)
    except Exception as e:
        logger.exception(e)
    return True


async def on_startup(dsp: Dispatcher):
    logger.info("Is starting...")

    bot_info = await dsp.bot.me
    tbot_info = await tbot.get_me()

    await support.logger_conf.start(DEBUG_LOGGING)
    await plugins.initialize_plugins()
    await utils.initialize_utils()

    logger.info(f"Bot {bot_info.full_name} [@{bot_info.username}] started!")
    logger.info(f"Telethon session established for [@{tbot_info.username}]!")


async def on_shutdown(dsp: Dispatcher):
    logger.warning("Shutting down...")

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection
    await dsp.storage.close()
    await dsp.storage.wait_closed()

    logger.info("Bye bye!")


if __name__ == "__main__":
    tbot.start()
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
