from support import types
from support.bots import dp


@dp.message_handler(is_chat_admin=True, commands="help", commands_prefix="!")
async def help_command(message: types.Message):
    await message.answer("Тут може бути текст допомоги")
