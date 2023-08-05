from aiogram import md, types
from support.bots import dp, bot
from loguru import logger
from support.redis_db import db


@dp.message_handler(commands="leaderboard", commands_prefix="!")
async def leaderboard(message: types.Message):
    """Show the leaderboard of the chat"""
    chat_id = str(message.chat.id)
    args = message.text.split()
    if len(args) >= 2:
        if not db.exists("leaderboard"):
            await message.answer("No global leaderboard yet")
            return
        if args[1] == "global":
            data = db.hgetall("leaderboard")
            sorted_data = sorted(data.items(), key=lambda x: int(x[1]), reverse=True)
            text = '🏆 Міжнародний Мемо-Фонд "Фелікс-мемокрад" 🏆\n\n'
        else:
            sorted_data = []
            text = ""
            await message.answer('Unrecognized !leaderboard param(s). Try "global"')
    else:
        if not db.exists(chat_id):
            await message.answer("No leaderboard yet")
            return
        data = db.hgetall(chat_id)
        sorted_data = sorted(data.items(), key=lambda x: int(x[1]), reverse=True)
        text = '🏆 Благодійний фонд ТОВ "Фелікс-мемокрад" 🏆\n\n'

    medals = ["🥇", "🥈", "🥉"]
    for i, item in enumerate(sorted_data):
        key = int(item[0])
        count = int(item[1])
        user_id = int(key)
        user = await bot.get_chat_member(chat_id, user_id)
        try:
            name = user.user.full_name or f"{user.user.username}"
        except Exception as e:
            logger.error(e)
            name = key

        medal = medals[i] if i < 3 else f"{i + 1:02d}"
        text += f"{medal}》👤 {md.hlink(name, f'https://t.me/{user.user.username}')}. Вкрадено {count} раз(ів)\n"
    await message.answer(text, parse_mode="HTML", disable_web_page_preview=True)


async def on_startup():
    """Plugin shows the leaderboard of the chat"""
    logger.trace("leaderboard.py loaded")
