from loguru import logger
import asyncio
from support.bots import bot
from utils.media_sync import media_files
from plugins.channel.configs import followers_conf
import random
import aiogram

channel_id = followers_conf.CHANNEL_ID
update_interval = 5
last_gif = None


async def track_channel_member_count(channel: str, interval: int):
    previous_member_count = await bot.get_chat_member_count(channel)
    logger.debug(f"Current subscribers count: {previous_member_count}")
    while True:
        member_count = await bot.get_chat_member_count(channel)
        if member_count > previous_member_count:
            logger.debug(f"New subscriber. New subscribers count: {member_count}")
            await post_new_follower_media()
            previous_member_count = member_count
        elif member_count < previous_member_count:
            logger.debug(f"Somebody left. New subscribers count: {member_count}")
            await post_leave_follower_media()
            previous_member_count = member_count
        await asyncio.sleep(interval)


async def post_new_follower_media():
    global last_gif
    gifs = [
        file_path
        for folder in media_files.values()
        for file_path in folder.values()
        if followers_conf.NF_FORMAT in file_path
    ]
    gif = random.choice(gifs)
    while gif == last_gif:
        gif = random.choice(gifs)
    last_gif = gif
    # await bot.send_animation(channel_id, open(gif, "rb"))
    logger.debug("post_new_follower_gif()")


async def post_leave_follower_media():
    logger.debug("post_leave_follower_gif()")


async def on_startup():
    asyncio.create_task(track_channel_member_count(channel_id, update_interval))
    logger.debug("followers.py loaded")
