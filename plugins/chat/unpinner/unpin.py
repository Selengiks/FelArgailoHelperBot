from plugins import types, logger, asyncio
from support.bots import bot, dp


@dp.message_handler(
    lambda message: message.from_user.id == 777000,
    content_types=[types.ContentType.ANY],
)
async def handle_and_unpin(update: types.Update):
    chat = await dp.bot.get_chat(update.chat.id)
    channel = await dp.bot.get_chat(chat.linked_chat_id)
    pinned_message = chat.pinned_message

    is_empty = True
    try_attempt = 10
    while is_empty:
        if pinned_message is None:
            for i in range(1, try_attempt + 1):
                await asyncio.sleep(2)
                chat = await dp.bot.get_chat(update.chat.id)
                pinned_message = chat.pinned_message
                logger.warning(f"Attempt {i}: Pinned message is {pinned_message}")
            message = (
                f"Cannot unpin message via unexpected error, "
                f"still get {pinned_message} after {try_attempt} attempts"
            )
            await bot.send_message(chat.id, message)
            logger.warning("Message not unpinned")
            return False
        else:
            is_empty = False

    if pinned_message.from_id == channel.id:
        await dp.bot.unpin_chat_message(
            chat_id=chat.id, message_id=pinned_message.message_id
        )
        logger.debug(
            f"\n[Message] Message with id [{pinned_message.message_id}]\n"
            f"    ID: {pinned_message.message_id}\n"
            f"    From:{pinned_message.from_id}\n"
            f"    Url: {pinned_message.url}\n"
            f"    From: https://t.me/{pinned_message.sender_chat.username}/{pinned_message.forward_from_message_id}\n"
            f"Successfully unpinned!"
        )
        await asyncio.sleep(1)

    elif update.from_id == channel.id:
        await dp.bot.unpin_chat_message(chat_id=chat.id, message_id=update.message_id)
        logger.debug(
            f"\n[Update] Message\n"
            f"    ID: {pinned_message.message_id}\n"
            f"    From:{pinned_message.from_id}\n"
            f"    Url: {pinned_message.url}\n"
            f"    From: https://t.me/{pinned_message.sender_chat.username}/{pinned_message.forward_from_message_id}\n"
            f"Successfully unpinned!"
        )
        await asyncio.sleep(1)


async def on_startup():
    logger.trace("unpin.py loaded")
