from aiogram.dispatcher.filters import BoundFilter
from support.bots import dp
import config


class IsAdminFilter(BoundFilter):
    key = "is_admin"

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message):
        return message.from_user.id in config.ADMINS


dp.filters_factory.bind(IsAdminFilter, event_handlers=[dp.message_handlers])
