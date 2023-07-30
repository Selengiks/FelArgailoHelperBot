import os
from aiogram import types
from loguru import logger
from dotenv import load_dotenv
from utils import sender

load_dotenv()
channel_id = os.getenv("CHANNEL")


@dp.message_handler(is_admin=True, is_reply=True, commands="steal", commands_prefix="!")
async def stealer(message: types.Message):
    """Via command send replied media or text to target channel"""
    if message.reply_to_message:
        answer = message.reply_to_message
        try:
            await sender.send_data(
                answer,
                channel_id,
                disable_web_page_preview=True,
            )
        except Exception as e:
            logger.error(e)
    msg = f"Data has been stolen successfully!"
    logger.debug(msg)
    await message.answer(msg)


async def on_startup():
    """Plugin allow you, via command send somebody messages or media to your channel"""
    logger.debug("stealer.py loaded")
