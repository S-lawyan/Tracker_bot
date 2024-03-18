from apscheduler.schedulers.async_ import AsyncScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from scheduler.wb_tracker import WildberriesTracker
# from scheduler.ozon_tracker import OzonTracker
import asyncio

class SchedulerService:
    def __init__(
            self,
            scheduler: AsyncScheduler,
            wb_tracker: WildberriesTracker,
            # ozon_tracker: OzonTracker,
    ):