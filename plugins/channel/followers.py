from plugins import os, logger, asyncio
import random
from support.bots import bot
from support.telebot import tbot
from utils.media_sender import send_media
from utils.media_sync import media_files


channel_id = os.getenv("CHANNEL")
last_media = None


async def get_latest_users():
    """Return dict with lists of joined and left users from Admin log (need Telethon)"""
    latest_join = [
        user.user.username
        for user in (await tbot.get_admin_log(channel_id, join=True))[:5]
    ]
    latest_left = [
        user.user.username
        for user in (await tbot.get_admin_log(channel_id, leave=True))[:5]
    ]
    return {"joined": latest_join, "left": latest_left}


async def track_channel_member_count():
    """Track channel subscribers count and do post_new_follower_media() or post_leave_follower_media() if it
    increased or decreased"""
    previous_member_count = await bot.get_chat_member_count(channel_id)
    logger.info(f"Tracking channel [{channel_id}]...")
    logger.debug(f"Current subscribers count: {previous_member_count}")
    while True:
        try:
            member_count = await bot.get_chat_member_count(channel_id)
            latest_users = await get_latest_users()
            if member_count > previous_member_count:
                logger.debug(f"New subscriber. New subscribers count: {member_count}")
                if (
                    latest_users["joined"][0] not in latest_users["left"]
                ):  # prevent spam by leave\join
                    await post_new_follower_media()
                else:
                    logger.warning(
                        "Spam attempt avoided for post_new_follower_media()\n"
                        f"Latest joined users:\n{latest_users['joined']}\n"
                        f"Latest left users\n{latest_users['left']}"
                    )

                previous_member_count = member_count
            elif member_count < previous_member_count:
                logger.debug(f"Somebody left. New subscribers count: {member_count}")
                if (
                    latest_users["left"][0] not in latest_users["joined"]
                ):  # prevent spam by leave\join
                    await post_leave_follower_media()
                else:
                    logger.warning(
                        "Spam attempt avoided for post_leave_follower_media()\n"
                        f"Latest joined users:\n{latest_users['joined']}\n"
                        f"Latest left users\n{latest_users['left']}"
                    )
                previous_member_count = member_count
            await asyncio.sleep(60)
        except Exception as e:
            logger.error(f"Error occured! Some details: {e}")


async def post_new_follower_media():
    """Post welcome media for new followers"""
    global last_media
    medias = [
        file["Path"]
        for folder in media_files.values()
        for file in folder
        if "new_follower_" in os.path.splitext(file["Path"])[0]
    ]
    media = random.choice(medias)
    while media == last_media:
        media = random.choice(medias)
    last_media = media
    await asyncio.sleep(10)
    await send_media(bot, channel_id, media)
    logger.debug("post_new_follower_media()")


async def post_leave_follower_media():
    """Post media if somebody left the channel. Now do nothing"""
    logger.debug("post_leave_follower_media()")


async def on_startup():
    """Plugin allow you track subscribers count from channel and do different things, based on it"""
    asyncio.create_task(track_channel_member_count())
    logger.trace("followers.py loaded")
