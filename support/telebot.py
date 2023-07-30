import os
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

tbot = TelegramClient("anon", int(os.getenv("API_ID")), os.getenv("API_HASH"))
