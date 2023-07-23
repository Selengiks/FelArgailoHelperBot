import os
from dotenv import load_dotenv

from loguru import logger

load_dotenv()

# Base telegram setting
POLLING = os.getenv("POLLING")  # if True - polling mode, False - webhook mode
LOCAL_SERVER_URL = (
    os.getenv("LOCAL_SERVER_URL") or None
)  # url for local server, Details on: https://core.telegram.org/bots/api#using-a-local-bot-api-server

# Telegram bot data
BOT_TOKEN = os.getenv("BOT_TOKEN")


# Webhook settings
if not POLLING == "True":
    # Webhook
    WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")
    WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")

    # Web app
    WEBAPP_HOST = os.getenv("WEBAPP_HOST")
    WEBAPP_PORT = os.getenv("WEBAPP_PORT", default=8000)

ADMINS = ["290522978"]  # list of admins, who can administer bot

logger.debug("Bot config applied")
