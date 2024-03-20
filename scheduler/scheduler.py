from apscheduler.schedulers.async_ import AsyncScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from scheduler.wb_tracker import WildberriesTracker
# from scheduler.ozon_tracker import OzonTracker
import asyncio
from loguru import logger


class SchedulerService:
    def __init__(
            self,
            scheduler: AsyncScheduler,
            wb_tracker: WildberriesTracker,
            # ozon_tracker: OzonTracker,
    ):
        self.scheduler = scheduler
        self.wb_tracker = wb_tracker
        # self.ozon_tracker = ozon_tracker

    async def start(self):
        # Планирование тасков и запуск планировщика
        # TODO попробовать переделать планировщик под релизную версию библиотеки
        #  и проверить будет ли работать асинхронно, чтобы избавиться от костыля в _wb_tracking_scheduler
        # await self.scheduler.add_schedule(
        #     _wb_tracking_scheduler,
        #     "interval",
        #     seconds=5,
        # )

        # С костылем, но работает
        await self._wb_tracking_scheduler()
        await self.scheduler.start_in_background()
        logger.warning("Планировщик запущен!")

    async def _wb_tracking_scheduler(self,):
        while True:
            logger.info("Старт проверки цен через 5 секунд")
            await asyncio.sleep(5)
            await self.wb_tracker.tracking()
            await asyncio.sleep(5)


async def _ozon_tracking_scheduler():
    # Планирование отслеживания ВБ
    pass
