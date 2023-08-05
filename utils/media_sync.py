import os
import asyncio
from aiogram import types
from loguru import logger
import hashlib
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
    medialist_message = ""
    for folder, files in media_files.items():
        medialist_message += f"В /{folder}:\n"
        for file in files:
            medialist_message += f"{file}\n"
        medialist_message += "\n"
    await message.answer(medialist_message)


@dp.message_handler(is_admin=True, is_reply=True, commands="add", commands_prefix="!")
async def add_media(message: types.Message):
    """Add media files to bot"""
    if message.reply_to_message:
        answer = message.reply_to_message
        # Get the folder and file name from the command arguments or use default values
        args = message.text.split()
        if len(args) > 2:
            folder = args[1]
            file_name = args[2]
            # Check if the folder exists
            folder_path = os.path.join(media_folder, folder)
            if not os.path.exists(folder_path):
                await message.answer(
                    f"Folder {folder} doesn't exist. Enter exist folder."
                )
                return
            # Get the file extension from the replied message
            file_extension = ""
            if answer.document:
                file_extension = os.path.splitext(answer.document.file_name)[1]
                file_id = answer.document.file_id
            elif answer.photo:
                file_extension = ".jpg"
                file_id = answer.photo[-1].file_id
            elif answer.video:
                file_extension = ".mp4"
                file_id = answer.video.file_id
            elif answer.voice:
                file_extension = ".ogg"
                file_id = answer.voice.file_id
            elif answer.audio:
                file_extension = os.path.splitext(answer.audio.file_name)[1]
                file_id = answer.audio.file_id
            elif answer.sticker:
                file_extension = ".webp"
                file_id = answer.sticker.file_id
            elif answer.animation:
                file_extension = ".mp4"
                file_id = answer.animation.file_id
            else:
                await message.answer("Unsupported file type")
                return
            # Check if a file with the same name already exists and add a number to the file name if necessary
            i = 1
            while os.path.exists(
                os.path.join(folder_path, f"{file_name}_{i}{file_extension}")
            ):
                i += 1
            file_name = f"{file_name}_{i}{file_extension}"
            # Download the file and save it to the specified folder
            await (await dp.bot.get_file(file_id)).download(
                os.path.join(folder_path, file_name)
            )

            # Check for duplicates
            duplicates = is_duplicate(
                file_name, os.path.join(folder_path, file_name), folder_path
            )
            if duplicates:
                await message.answer(
                    f"Duplicated file{'s' if len(duplicates) > 1 else ''} {', '.join(duplicates)}. Not added."
                )
                os.remove(os.path.join(folder_path, file_name))

            else:
                await message.answer(
                    f"File {file_name} successfully added to folder {folder}!"
                )
                await sync_media()
        else:
            await message.answer(
                "Specify folder and file name in format `!add <folder> <file_name>`"
            )


@dp.message_handler(is_admin=True, commands="edit", commands_prefix="!")
async def edit_media(message: types.Message):
    """Edit media files to bot"""
    pass


@dp.message_handler(is_admin=True, commands="delete", commands_prefix="!")
async def delete_media(message: types.Message):
    """Delete media files from bot"""
    args = message.text.split()
    if len(args) > 1:
        file_name = args[1]
        folder_path = "media"
        file_deleted = False
        for root, dirs, files in os.walk(folder_path):
            file_path = os.path.join(root, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
                await message.answer(
                    f"File {file_name} successfully deleted from folder {root}."
                )
                file_deleted = True
        if not file_deleted:
            await message.answer(f"File {file_name} not found.")
            await sync_media()
    else:
        await message.answer("Enter file name in full format (example_1.mp4.")


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


def get_file_hash(file_path):
    """Calculate the SHA256 hash of a file"""
    with open(file_path, "rb") as f:
        file_hash = hashlib.sha256()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()


def is_duplicate(file_name, file_path, folder_path):
    """Check if a file is a duplicate of an existing file in a folder"""
    # Calculate the hash of the file
    file_hash = get_file_hash(file_path)
    # Create a list to store the duplicates
    duplicates = []
    # Check if any of the existing files in the folder have the same hash
    for root, dirs, files in os.walk("media"):
        for file in files:
            existing_file_path = os.path.join(root, file)
            if file_name in existing_file_path:
                continue
            existing_file_hash = get_file_hash(existing_file_path)
            if file_hash == existing_file_hash:
                duplicates.append(file)
    return duplicates


async def on_startup():
    asyncio.create_task(sync_media())
    logger.trace("media_sync loaded")
