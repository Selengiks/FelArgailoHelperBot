import os
import asyncio
from loguru import logger
from run import DEBUG_LOGGING

media_folder = "media"
media_files = {}


async def sync_media():
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

        # Add files
        for folder, files in new_media_files.items():
            if folder not in media_files:
                media_files[folder] = {}
            for file, file_path in files.items():
                media_files[folder][file] = file_path

        # Remove files
        for folder, files in list(media_files.items()):
            for file in list(files):
                if folder not in new_media_files or file not in new_media_files[folder]:
                    del media_files[folder][file]
            if not media_files[folder]:
                del media_files[folder]
        if DEBUG_LOGGING:
            for k, v in media_files.items():
                logger.debug(f"Files sync result:\nKey: {k}. Values: {v}")
        await asyncio.sleep(60)


async def on_startup():
    asyncio.create_task(sync_media())
    logger.debug("media_sync loaded")
