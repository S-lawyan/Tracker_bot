import sqlite3 as sq
from bot.config import Settings
from loguru import logger


class SQLiteBase:
    def __init__(self, config: Settings):
        self.connect = sq.connect(
            database="../database/" + config.db.db_filename
        )
        self.cursor = self.connect.cursor()
        if self.connect:
            logger.info("The connection to the database has been completed successfully!")
            self._create_scheme()

    def _create_scheme(self):
        """Создание схемы БД"""
        with self.connect as connect:
            pass
