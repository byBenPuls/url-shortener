import logging
import typing

import redis.asyncio as redis
from src.settings import settings
logger = logging.getLogger(__name__)


class RedisPool:
    def __init__(self) -> None:
        self.pool = None

    async def create_connection(self) -> None:
        logger.debug('Trying to connect..')
        client = redis.ConnectionPool(host=settings.REDIS_HOST,
                                      port=settings.REDIS_PORT,
                                      password=settings.REDIS_PASSWORD,
                                      db=settings.REDIS_DB)
        self.pool = redis.Redis.from_pool(client)
        logging.info(str(await self.pool.get('123')))
        logging.debug('Successfully connected!')

    async def get_connection(self) -> typing.Optional[redis.Redis]:
        return self.pool

    async def close_connection(self):
        self.pool.aclose()
