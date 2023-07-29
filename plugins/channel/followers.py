from loguru import logger
import asyncio
from support.bots import bot
from support.telebot import tbot
from utils.media_sync import media_files
from plugins.channel.configs import followers_conf
import random

channel_id = followers_conf.CHANNEL_ID
last_gif = None


async def get_latest_users():
    """Return dict with lists of joined and left users from Admin log (need Telethon)"""
    latest_join = [
        user.user.username
        for user in (await tbot.get_admin_log(channel_id, join=True))[:10]
    ]
    latest_left = [
        user.user.username
        for user in (await tbot.get_admin_log(channel_id, leave=True))[:10]
    ]
    return {"joined": latest_join, "left": latest_left}


async def track_channel_member_count():
    """Track channel subscribers count and do post_new_follower_media() or post_leave_follower_media() if it
    increased or decreased"""
    previous_member_count = await bot.get_chat_member_count(channel_id)
    logger.info(f"Tracking channel [{channel_id}]...")
    logger.debug(f"Current subscribers count: {previous_member_count}")
    while True:
        member_count = await bot.get_chat_member_count(channel_id)
        latest_users = await get_latest_users()
        if member_count > previous_member_count:
            logger.debug(f"New subscriber. New subscribers count: {member_count}")
            if (
                latest_users["joined"][0] not in latest_users["left"]
            ):  # prevent spam by leave\join
                await post_new_follower_media()
            else:
                logger.debug(f"Spam attempt avoided for post_new_follower_media()")

            previous_member_count = member_count
        elif member_count < previous_member_count:
            logger.debug(f"Somebody left. New subscribers count: {member_count}")
            if (
                latest_users["left"][0] not in latest_users["joined"]
            ):  # prevent spam by leave\join
                await post_leave_follower_media()
            else:
                logger.debug(f"Spam attempt avoided for post_leave_follower_media()")
            previous_member_count = member_count
        await asyncio.sleep(60)


async def post_new_follower_media():
    """Post welcome media for new followers"""
    global last_gif
    gifs = [
        file_path
        for folder in media_files.values()
        for file_path in folder.values()
        if followers_conf.NF_FORMAT
        in file_path  # to change naming for file, edit NF_FORMAT in followers_conf file
    ]
    gif = random.choice(gifs)
    while gif == last_gif:
        gif = random.choice(gifs)
    last_gif = gif
    await asyncio.sleep(10)
    await bot.send_animation(channel_id, open(gif, "rb"))
    logger.debug("post_new_follower_gif()")


async def post_leave_follower_media():
    """Post media if somebody left the channel. Now do nothing"""
    logger.debug("post_leave_follower_gif()")


async def on_startup():
    """Plugin allow you track subscribers count from channel and do different things, based on it"""
    asyncio.create_task(track_channel_member_count())
    logger.debug("followers.py loaded")
