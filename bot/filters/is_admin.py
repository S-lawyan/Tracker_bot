from typing import Union

from aiogram.dispatcher.filters import BoundFilter
from bot.config import config
from loguru import logger
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineQuery,
)


class IsAdmin(BoundFilter):
    async def check(self, obj: Union[Message, CallbackQuery, InlineQuery]):
        if isinstance(obj, Message):
            user_id = obj.from_user.id
        elif isinstance(obj, CallbackQuery):
            user_id = obj.from_user.id
        elif isinstance(obj, InlineQuery):
            user_id = obj.from_user.id
        else:
            user_id = None

        return user_id in list(config.bot.admins)
