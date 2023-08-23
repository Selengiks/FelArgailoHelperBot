import os
from aiogram import types
from support.bots import dp
from loguru import logger
from dotenv import load_dotenv
from utils import message_sender
from support.redis_db import db

load_dotenv()
channel_id = os.getenv("CHANNEL")


@dp.message_handler(is_admin=True, is_reply=True, commands="steal", commands_prefix="!")
async def stealer(message: types.Message):
    if message.reply_to_message:
        answer = message.reply_to_message
        args = message.text.split()
        tag = "#meme"
        if len(args) > 1:
            if args[1].startswith("#"):
                tag = args[1]
                caption = f"Вкрадено у @{answer.from_user.username or answer.from_user.full_name}\n\n{tag}"
            elif args[1] == "-r":
                caption = " ".join(args[2:])
                if not any(word.startswith("#") for word in caption.split()):
                    caption += f"\n\n{tag}"

                if f"@{answer.from_user.username}" not in caption:
                    caption += f", від пана @{answer.from_user.username or answer.from_user.full_name}"
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
                user = answer.from_user

                # Local leaderboards
                if not db.exists(f"leaderboard:local:{chat_id}:{user.id}:score_l"):
                    db.sadd(
                        f"leaderboard:local:{chat_id}:{user.id}:id",
                        user.id,
                    )
                    db.sadd(
                        f"leaderboard:local:{chat_id}:{user.id}:username",
                        user.mention,
                    )
                    db.sadd(
                        f"leaderboard:local:{chat_id}:{user.id}:full_name",
                        user.full_name,
                    )
                    db.zadd(
                        f"leaderboard:local:{chat_id}:{user.id}:score_l", {"score_l": 1}
                    )

                else:
                    if (
                        db.zcard(f"leaderboard:local:{chat_id}:{user.id}:score_l")
                        is None
                    ):
                        db.zadd(
                            f"leaderboard:local:{chat_id}:{user.id}:score_l",
                            {"score_l": 1},
                        )
                    else:
                        db.zincrby(
                            f"leaderboard:local:{chat_id}:{user.id}:score_l",
                            1,
                            "score_l",
                        )

                # Global leaderboards
                if not db.exists(f"leaderboard:global:{user.id}:score_g"):
                    db.sadd(
                        f"leaderboard:global:{user.id}:id",
                        user.id,
                    )
                    db.sadd(
                        f"leaderboard:global:{user.id}:username",
                        user.mention,
                    )
                    db.sadd(
                        f"leaderboard:global:{user.id}:full_name",
                        user.full_name,
                    )
                    db.zadd(f"leaderboard:global:{user.id}:score_g", {"score_g": 1})

                else:
                    if db.zcard(f"leaderboard:global:{user.id}:score_g") is None:
                        db.zadd(f"leaderboard:global:{user.id}:score_g", {"score_g": 1})
                    else:
                        db.zincrby(
                            f"leaderboard:global:{user.id}:score_g", 1, "score_g"
                        )

            except Exception as e:
                logger.error(e)

        except Exception as e:
            logger.error(e)

    msg = f"Data has been stolen successfully!"
    logger.debug(msg)


async def on_startup():
    logger.trace("stealer.py loaded")
