import os
import asyncio
from loguru import logger

media_folder = "media"
media_files = {}


async def sync_media():
    while True:
        new_media_files = {}
        for root, dirs, files in os.walk(media_folder):
            for file in files:
                # Ігнорувати файли без розширення або без імені
                if not os.path.splitext(file)[0] or not os.path.splitext(file)[1]:
                    continue
                folder = os.path.basename(root)
                if folder not in new_media_files:
                    new_media_files[folder] = []
                new_media_files[folder].append(file)

        # Add files
        for folder, files in new_media_files.items():
            if folder not in media_files:
                media_files[folder] = []
            for file in files:
                if file not in media_files[folder]:
                    media_files[folder].append(file)

        # Remove files
        for folder, files in list(media_files.items()):
            for file in files:
                if folder not in new_media_files or file not in new_media_files[folder]:
                    media_files[folder].remove(file)
            if not media_files[folder]:
                del media_files[folder]

        await asyncio.sleep(60)


async def on_startup():
    asyncio.create_task(sync_media())
    logger.debug("media_sync loaded")
