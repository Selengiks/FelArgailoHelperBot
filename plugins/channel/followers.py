from loguru import logger
import asyncio
from support.bots import dp, bot
import random

channel_id = "@felixfantastic1"
update_interval = 30


async def track_channel_member_count(channel: str, interval: int):
    previous_member_count = await bot.get_chat_member_count(channel)
    while True:
        member_count = await bot.get_chat_member_count(channel)
        if member_count > previous_member_count:
            logger.debug(member_count)  # Add normal log message
            await post_new_follower_gif()
            previous_member_count = member_count
        elif member_count < previous_member_count:
            logger.debug(member_count)  # Add normal log message
            await post_leave_follower_gif()
            previous_member_count = member_count
        await asyncio.sleep(interval)


async def post_new_follower_gif():
    logger.debug("post_new_follower_gif()")


async def post_leave_follower_gif():
    logger.debug("post_leave_follower_gif()")


async def on_startup():
    asyncio.create_task(track_channel_member_count(channel_id, update_interval))
    logger.debug("followers.py loaded")
