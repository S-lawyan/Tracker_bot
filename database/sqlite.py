import json
import sqlite3 as sq
from typing import Any

from bot.config import Settings
from loguru import logger
from bot.utils.models import Product
from bot.utils.exceptions import (
    DatabaseExecuteQueryError,

)


class SQLiteBase:
    def __init__(self, config: Settings):
        self.connect = sq.connect(
            database="../database/" + config.db.db_filename
        )
        if self.connect:
            logger.warning("The connection to the database has been completed successfully!")
            self._create_scheme()

    def _create_scheme(self) -> None:
        """Создание схемы БД"""
        with self.connect as connect:
            connect.execute("""
                CREATE TABLE IF NOT EXISTS "products" (
                    "id"	INTEGER,
                    "user_id"	INTEGER,
                    "article"	INTEGER,
                    "data"	TEXT,
                    PRIMARY KEY("id" AUTOINCREMENT)
                )
            """)
            connect.execute("""
                CREATE TABLE IF NOT EXISTS "settings" (
                    "user_id"	INTEGER UNIQUE,
                    "difference "	INTEGER DEFAULT 10
                )
            """)
            connect.commit()

    async def _execute_query(self, query: str, params: tuple = None) -> Any:
        try:
            with self.connect as connect:
                result = connect.execute(query, params)
                connect.commit()
                return result
        except (Exception,) as exc:
            logger.error(f"Ошибка запроса к БД: {query}\nОшибка: {exc}")
            raise DatabaseExecuteQueryError()

    async def insert_user(self, user_id: int) -> None:
        query = f"""
            INSERT INTO settings (
                user_id
            ) 
            VALUES (?)
        """
        params = (user_id,)
        await self._execute_query(query=query, params=params)

    async def check_user(self, user_id: int) -> bool:
        with self.connect as connect:
            return bool(
                connect.execute(
                    "SELECT EXISTS(SELECT 1 FROM settings WHERE user_id = ?)", (user_id,)
                ).fetchone()[0]
            )

    async def insert_product(self, product: Product, user_id: int) -> None:
        query = f"""
            INSERT INTO products (
                user_id, 
                article, 
                data
            ) 
            VALUES (?, ?, ?)
        """
        params = (user_id, product.article, json.dumps(product.__dict__, ensure_ascii=False))
        await self._execute_query(query=query, params=params)

