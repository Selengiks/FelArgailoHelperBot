import asyncio

from aiogram import types
from support.bots import dp, bot
from loguru import logger
from support.redis_db import db


async def get_user(chat_id, user_id):
    user = await bot.get_chat_member(chat_id, user_id)
    try:
        name = user.user.full_name or f"{user.user.username}"
    except Exception as e:
        logger.error(e)
        name = user_id
    return name


@dp.message_handler(commands="leaderboard", commands_prefix="!")
async def leaderboard(message: types.Message):
    """Show the leaderboard of the chat"""
    chat_id = str(message.chat.id)
    args = message.text.split()
    if len(args) >= 2:
        if args[1] == "global":
            # Отримайте всі ключі, які закінчуються на :score_g
            cursor = 0
            keys = []
            while True:
                cursor, new_keys = db.scan(
                    cursor=cursor, match="leaderboard:global:*:score_g"
                )
                keys.extend(new_keys)
                if cursor == 0:
                    break

            data = {}
            for key in keys:
                # Отримайте значення score_g для кожного ключа
                user_id = key.split(":")[2]
                score_g = int(
                    db.zscore(f"leaderboard:global:{user_id}:score_g", "score_g")
                )
                data[key] = score_g

            sorted_data = sorted(data.items(), key=lambda x: int(x[1]), reverse=True)
            if not sorted_data:
                text = "No global leaderboard yet"
            else:
                text = '🏆 Міжнародний Мемо-Фонд "Фелікс-мемокрад" 🏆\n\n'
        else:
            sorted_data = []
            text = ""
            await message.answer(
                'Unrecognized !leaderboard param(s). Try "!leaderboard global"'
            )
    else:
        # Отримайте всі ключі, які закінчуються на :score_l
        cursor = 0
        keys = []
        while True:
            cursor, new_keys = db.scan(
                cursor=cursor, match=f"leaderboard:local:{chat_id}:*:score_l"
            )
            keys.extend(new_keys)
            if cursor == 0:
                break

        data = {}
        for key in keys:
            # Отримайте значення score_l для кожного ключа
            user_id = key.split(":")[3]
            score_l = db.zscore(
                f"leaderboard:local:{chat_id}:{user_id}:score_l", "score_l"
            )
            data[key] = score_l

        sorted_data = sorted(data.items(), key=lambda x: int(x[1]), reverse=True)
        if not sorted_data:
            text = "No local leaderboard yet"
        else:
            text = '🏆 Благодійний фонд ТОВ "Фелікс-мемокрад" 🏆\n\n'

    if sorted_data:
        medals = ["🥇", "🥈", "🥉"]
        for i, item in enumerate(sorted_data):
            key = item[0]
            count = int(item[1])
            # Отримайте user_id з ключа
            user_id = int(key.split(":")[-2])
            user = await bot.get_chat_member(chat_id, user_id)
            try:
                name = user.user.full_name or f"{user.user.username}"
            except Exception as e:
                logger.error(e)
                name = key

            medal = medals[i] if i < 3 else f"{i + 1:02d}"
            text += f"{medal}》👤 {name}. Вкрадено {count} раз(ів)\n"
    sent_message = await message.answer(
        text, parse_mode="HTML", disable_web_page_preview=True
    )
    await asyncio.sleep(1)

    # Edit the message to add links to user profiles
    if sorted_data:
        text_with_links = text
        for i, item in enumerate(sorted_data):
            key = item[0]
            # Отримайте user_id з ключа
            user_id = int(key.split(":")[-2])
            name = await get_user(chat_id, user_id)

            text_with_links = text_with_links.replace(
                f"👤 {name}", f'👤 <a href="tg://user?id={user_id}">{name}</a>'
            )
        await sent_message.edit_text(
            text_with_links, parse_mode="HTML", disable_web_page_preview=True
        )


async def on_startup():
    """Plugin shows the leaderboard of the chat"""
    logger.trace("leaderboard.py loaded")
