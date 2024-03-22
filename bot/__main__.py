import asyncio

from bot.services import dp
from scheduler.wb_tracker import WildberriesTracker
# from bot.services import OZON_track
from loguru import logger
from aiogram import executor
import handlers
from aiogram import types
from bot import filters
from apscheduler.schedulers.async_ import AsyncScheduler
from scheduler.scheduler import SchedulerService
from bot.services import HttpSessionMaker


async def set_default_settings_bot(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Главное меню"),
            types.BotCommand("help", "Помощь"),
            types.BotCommand("truncate", "Очистить позиции"),
        ]
    )


async def start_schedulers(WB):
    async with AsyncScheduler() as scheduler:
        service_scheduler = SchedulerService(
            scheduler=scheduler,
            wb_tracker=WB
        )
        await service_scheduler.start()
        # while True:
        #     await asyncio.sleep(1)


async def on_startup(dp):
    logger.add(
        "logs/avia_bot_{time:YYYY-MM-DD}.log",
        rotation="1 day",
        retention="7 days",
        compression="zip",
        level="DEBUG",
    )
    await set_default_settings_bot(dp=dp)
    logger.warning("The bot is started!")


async def on_shutdown(dp):
    logger.warning("The bot is stop!")


def main():
    loop = asyncio.get_event_loop()
    WB: WildberriesTracker = WildberriesTracker(http_session_maker=HttpSessionMaker())
    # OZON: OzonTracker = OzonTracker(http_session_maker=HttpSessionMaker())
    # loop.create_task(start_schedulers(WB))
    filters.setup(dp=dp)
    executor.start_polling(dp, loop=loop, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)


if __name__ == "__main__":
    main()
