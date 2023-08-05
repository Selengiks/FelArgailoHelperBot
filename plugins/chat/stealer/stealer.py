import os
from aiogram import types
from support.bots import dp
from loguru import logger
from dotenv import load_dotenv
from utils import message_sender
from support.redis_db import db

load_dotenv()
channel_id = os.getenv("CHANNEL")
global_leaderboard = "leaderboard"


@dp.message_handler(is_admin=True, is_reply=True, commands="steal", commands_prefix="!")
async def stealer(message: types.Message):
    """Via command send replied media or text to target channel"""
    if message.reply_to_message:
        answer = message.reply_to_message
        args = message.text.split()
        tag = "#meme"
        if len(args) > 1:
            if args[1].startswith("#"):
                tag = args[1]
                caption = f"Вкрадено у @{answer.from_user.username or answer.from_user.full_name}\n\n{tag}"
            else:
                caption = " ".join(args[1:])
                if args[-1].startswith("#"):
                    tag = args[-1]
                    caption = f"{caption[:-len(tag)]}\n\n{tag}"
        else:
            caption = f"Вкрадено у @{answer.from_user.username or answer.from_user.full_name}\n\n{tag}"
        try:
            await message_sender.send_data(
                answer,
                channel_id,
                disable_web_page_preview=True,
                caption=caption,
            )
            try:
                chat_id = str(message.chat.id)
                user_id = str(answer.from_user.id)
                if not db.exists(chat_id):
                    db.hset(chat_id, user_id, 1)
                else:
                    count = db.hget(chat_id, user_id)
                    if count is None:
                        db.hset(chat_id, user_id, 1)
                    else:
                        db.hincrby(chat_id, user_id, 1)
            except Exception as e:
                logger.error(e)

        except Exception as e:
            logger.error(e)
    await update_leaderboard()
    msg = f"Data has been stolen successfully!"
    logger.debug(msg)


async def on_startup():
    """Plugin allow you, via command send somebody messages or media to your channel"""
    logger.trace("stealer.py loaded")


async def update_leaderboard():
    tables = db.keys()

    # Set db tables to exclude
    ignore_tables = [
        "archives",
        "audio",
        "documents",
        "gifs",
        "images",
        "videos",
    ]

    result = {}

    for table in tables:
        if table not in ignore_tables:
            data = db.hgetall(table)
            for key, value in data.items():
                if key in result:
                    result[key] += int(value)
                else:
                    result[key] = int(value)

    db.hset(global_leaderboard, result)
