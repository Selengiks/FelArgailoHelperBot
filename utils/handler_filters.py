from . import types
from aiogram.dispatcher.filters import BoundFilter
from support.bots import bot, dp
import config


class IsSuperAdminFilter(BoundFilter):
    key = "is_superadmin"

    def __init__(self, is_superadmin):
        self.is_superadmin = is_superadmin

    async def check(self, message):
        return message.from_user.id in config.ADMINS


class IsAdminFilter(IsSuperAdminFilter):
    key = "is_admin"

    async def check(self, message: types.Message):
        superadmin_check = await super().check(message)
        if superadmin_check:
            return True
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.is_chat_admin()


dp.filters_factory.bind(IsSuperAdminFilter, event_handlers=[dp.message_handlers])
dp.filters_factory.bind(IsAdminFilter, event_handlers=[dp.message_handlers])
