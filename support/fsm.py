from imports.global_imports import *
from typing import Optional

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from support.bots import bot, dp


# States
class Form(StatesGroup):
    primary = State()  # Will be represented in storage as 'Form:primary'
    main_menu = State()  # Will be represented in storage as 'Form:main_menu'
    settings = State()  # Will be represented in storage as 'Form:settings'


# You can use state '*' if you need to handle all states
@dp.message_handler(state="*", commands=["cancel"])
@dp.message_handler(lambda message: message.text.lower() == "cancel", state="*")
async def cancel_handler(
    message: types.Message, state: FSMContext, raw_state: Optional[str] = None
):
    """
    Allow user to cancel any action
    """
    if raw_state is None:
        return

    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply("Canceled.", reply_markup=types.ReplyKeyboardRemove())
