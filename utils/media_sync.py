import os
import asyncio
from aiogram import types
from loguru import logger
from support.bots import dp

try:
    from support.redis_db import db
except ImportError:
    logger.warning("Redis not enabled!")
from run import DEBUG_LOGGING

media_folder = "media"
media_files = {}


@dp.message_handler(is_admin=True, commands="media", commands_prefix="!")
async def media_list(message: types.Message):
    """Return media files list to chat"""
    await message.answer(str(media_files))


async def sync_media():
    """Checks the media folder and all sub-folders, and populates the dictionary
    with the files and their path in the format media_files = {"folder_name": {"file_name": path_to_file}}
    """
    while True:
        new_media_files = {}
        for root, dirs, files in os.walk(media_folder):
            for file in files:
                # Ignore file without name or extension
                if not os.path.splitext(file)[0] or not os.path.splitext(file)[1]:
                    continue
                folder = os.path.basename(root)
                if folder not in new_media_files:
                    new_media_files[folder] = {}
                file_path = os.path.join(root, file).replace("\\", "/")
                file_path = file_path[file_path.index(media_folder) :]
                new_media_files[folder][file] = file_path

        # Add files to Redis database
        for folder, files in new_media_files.items():
            try:
                db.hmset(folder, files)
            except NameError:
                logger.warning("Redis not enabled. Data not processed!")

        # Add files
        for folder, files in new_media_files.items():
            if folder not in media_files:
                media_files[folder] = {}
            for file, file_path in files.items():
                media_files[folder][file] = file_path

        # Remove files from Redis database
        for folder, files in list(media_files.items()):
            for file in list(files):
                if folder not in new_media_files or file not in new_media_files[folder]:
                    try:
                        db.hdel(folder, file)
                    except NameError:
                        logger.warning("Redis not enabled. Data not processed!")

        # Remove files
        for folder, files in list(media_files.items()):
            for file in list(files):
                if folder not in new_media_files or file not in new_media_files[folder]:
                    del media_files[folder][file]
            if not media_files[folder]:
                del media_files[folder]
        if DEBUG_LOGGING:
            logger.debug(f"Files sync result:")
            for k, v in media_files.items():
                logger.debug(f"Key: {k}.\nValues: {v}")
        await asyncio.sleep(3600)  # Set update interval in seconds (3600 = 1 hour)


async def on_startup():
    asyncio.create_task(sync_media())
    logger.trace("media_sync loaded")
