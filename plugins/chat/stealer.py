# stealer.py

import os
from aiogram import types
from support.bots import dp
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
        # Get the caption and tag from the command arguments or use default values
        args = message.text.split()
        tag = "#meme"
        if len(args) > 1:
            if args[1].startswith("#"):
                tag = args[1]
                caption = f"Вкрадено у {answer.from_user.username or answer.from_user.full_name}\n\n{tag}"
            else:
                caption = " ".join(args[1:])
                if args[-1].startswith("#"):
                    tag = args[-1]
                    caption = f"{caption[:-len(tag)]}\n\n{tag}"
        else:
            caption = f"Вкрадено у {answer.from_user.username or answer.from_user.full_name}\n\n{tag}"
        try:
            await sender.send_data(
                answer,
                channel_id,
                disable_web_page_preview=True,
                caption=caption,
            )
        except Exception as e:
            logger.error(e)
    msg = f"Data has been stolen successfully!"
    logger.debug(msg)
    await message.answer(msg)


async def on_startup():
    """Plugin allow you, via command send somebody messages or media to your channel"""
    logger.debug("stealer.py loaded")
