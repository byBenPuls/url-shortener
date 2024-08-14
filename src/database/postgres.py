import os
import logging
from typing import Optional

import asyncpg
from src.settings import settings
from pg_table_builder import Table, Column, Text, Serial

table = Table(
    'links',
    Column('id', Serial()),
    Column('original', Text()),
    Column('modified', Text())
)

# variable `table` returning SQL query for creation table, however has a type str
# library pg_table_builder doesn't have shielding from SQL injections because be careful

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, dsn: str = None, **kwargs) -> None:
        self.pool: Optional[asyncpg.Pool] = None
        self.dsn: dict = {'dsn': dsn}
        self.cfg: dict = kwargs

    async def get_connection(self) -> Optional[asyncpg.Pool]:
        """
        Returning database pool.

        Returns:
            In a case of success return pool else `None`
        """

        return self.pool

    async def connect(self) -> None:
        """
        Creating database pool

        Raises:
            Exception: If connection is not established then raising exception
        """
        logger.debug('Connecting to database..')
        self.pool = await asyncpg.create_pool(**(self.dsn if self.dsn is not None else self.cfg))
        if self.pool is None:
            raise ConnectionError('Cannot connect to database!')

        # creating table
        async with self.pool.acquire() as connection:
            await connection.execute(str(table))

    async def disconnect(self) -> None:
        """
        Closing database pool
        """
        if self.pool is not None:
            await self.pool.close()
            logger.debug('Connection closed')
        else:
            logger.warning('Cannot close database pool because pool is not created')


postgres = Database(dsn=settings.postgres_url)
