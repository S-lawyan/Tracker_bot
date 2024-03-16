from aiogram import Dispatcher
from .is_admin import IsAdmin


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsAdmin,
                            event_handlers=[dp.message_handlers, dp.callback_query_handlers, dp.inline_query_handlers])
