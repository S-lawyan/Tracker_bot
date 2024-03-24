from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from scheduler.wb_tracker import WildberriesTracker
# from scheduler.ozon_tracker import OzonTracker
import asyncio
from loguru import logger


class SchedulerService:
    def __init__(
            self,
            scheduler: AsyncIOScheduler,
            wb_tracker: WildberriesTracker,
            # ozon_tracker: OzonTracker,
    ):
        self.scheduler = scheduler
        self.wb_tracker = wb_tracker
        # self.ozon_tracker = ozon_tracker

    async def start(self):
        # Планирование тасков и запуск планировщика
        await self._wb_tracking_scheduler()
        self.scheduler.start()
        logger.warning("Планировщик запущен!")

    async def stop(self):
        await self.scheduler.shutdown()

    async def _wb_tracking_scheduler(self,):
        self.scheduler.add_job(
            self.wb_tracker.tracking,
            max_instances=5,
            coalesce=False,
            start_delay=10,
            misfire_grace_time=30,
            trigger=IntervalTrigger(
                # seconds=10,
                minutes=30,
            )
        )


async def _ozon_tracking_scheduler():
    # Планирование отслеживания ВБ
    pass
