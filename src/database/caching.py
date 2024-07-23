from src.database.redis import RedisPool

redis = RedisPool()


async def in_cache(key: str) -> bool:
    conn = await redis.get_connection()
    return await conn.get(key) is not None


async def record_in_cache(key: str, value: str) -> None:
    conn = await redis.get_connection()
    await conn.set(key, value)


async def get_from_cache(key: str) -> str:
    conn = await redis.get_connection()
    value = await conn.get(key)
    return value.decode('utf-8')
