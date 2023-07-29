from loguru import logger
import asyncio
from support.bots import dp
from aiogram import md, types


@dp.message_handler(is_admin=True, is_reply=True, commands="steal", commands_prefix="!")
async def stealer(message: types.Message):
    """Via command send replied media or text to target channel"""
    msg = f"Data has been stolen successfully!"
    logger.debug(msg)
    await message.answer(msg)  # WIP


async def on_startup():
    """Plugin allow you, via command send somebody messages or media to your channel"""
    logger.debug("stealer.py loaded")
