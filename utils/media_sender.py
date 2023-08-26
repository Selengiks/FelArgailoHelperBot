from . import logger, os


async def send_media(bot, channel_id, media):
    """Send media to channel based on file extension and folder"""
    ext = os.path.splitext(media)[1]
    folder = os.path.basename(os.path.dirname(media))
    if ext == ".gif" or (ext == ".mp4" and folder == "gifs"):
        await bot.send_animation(channel_id, open(media, "rb"))
    elif ext in [".jpg", ".jpeg", ".png"]:
        await bot.send_photo(channel_id, open(media, "rb"))
    elif ext == ".mp4":
        await bot.send_video(channel_id, open(media, "rb"))
    else:
        logger.warning(f"Unsupported media format: {ext}")
