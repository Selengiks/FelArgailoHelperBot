from plugins import types, logger, asyncio
from support.bots import dp


@dp.message_handler(
    lambda message: message.from_user.id == 777000,
    content_types=[types.ContentType.ANY],
)
async def handle_and_unpin(update: types.Update):
    chat = await dp.bot.get_chat(update.chat.id)
    channel = await dp.bot.get_chat(chat.linked_chat_id)
    pinned_message = chat.pinned_message

    is_empty = True
    while is_empty:
        if pinned_message is None:
            await asyncio.sleep(2)
            chat = await dp.bot.get_chat(update.chat.id)
            pinned_message = chat.pinned_message
            logger.warning(pinned_message)
        else:
            is_empty = False

    if pinned_message.from_id == channel.id:
        await dp.bot.unpin_chat_message(
            chat_id=chat.id, message_id=pinned_message.message_id
        )
        logger.debug(
            f"\n[Message] Message\n"
            f"[ID: {pinned_message.message_id}]\n"
            f"[Raw:{pinned_message}]\n"
            f"Successfully unpinned!"
        )

    elif update.from_id == channel.id:
        await dp.bot.unpin_chat_message(chat_id=chat.id, message_id=update.message_id)
        logger.debug(
            f"\n[Update] Message\n"
            f"[ID: {pinned_message.message_id}]\n"
            f"[Raw: {update}]\n"
            f"Successfully unpinned!"
        )


async def on_startup():
    logger.trace("unpin.py loaded")
