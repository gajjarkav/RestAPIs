import redis.asyncio as redis
from core.config import settings

pool = redis.ConnectionPool.from_url(url=settings.REDIS_URL, decode_responses=True)

async def get_redis():
    client = redis.Redis(connection_pool=pool)

    try:
        yield client
    finally:
        await client.close()