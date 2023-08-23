from aiogram import types
from loguru import logger
from support.bots import dp


@dp.message_handler(lambda message: message.from_user.id == 777000)
async def handle_and_unpin(update: types.Update):
    chat = await dp.bot.get_chat(update.chat.id)
    channel = await dp.bot.get_chat(chat.linked_chat_id)
    pinned_message = chat.pinned_message

    if pinned_message.from_id == channel.id:
        await dp.bot.unpin_chat_message(
            chat_id=chat.id, message_id=pinned_message.message_id
        )
        logger.debug(f"Message [{pinned_message.message_id}] successfully unpinned!")

    elif update.from_id == channel.id:
        await dp.bot.unpin_chat_message(chat_id=chat.id, message_id=update.message_id)
        logger.debug(f"Message [{pinned_message.message_id}] successfully unpinned!")


async def on_startup():
    logger.trace("unpin.py loaded")
