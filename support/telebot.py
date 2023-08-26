from imports.env_import import *
from telethon import TelegramClient

tbot = TelegramClient("anon", int(os.getenv("API_ID")), os.getenv("API_HASH"))
