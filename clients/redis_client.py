import logging

from redis.asyncio import Redis, ConnectionPool

from config.env_config import env_settings

logger = logging.getLogger(__name__)


class RedisClient:
    def __init__(self):
        self.client = None

    async def connect(self):
        logger.info("Connecting to Redis client...")
        redis_connection_pool = ConnectionPool(
            host=env_settings.REDIS_HOST,
            port=env_settings.REDIS_PORT,
            db=env_settings.REDIS_DB,
            decode_responses=True,
            max_connections=env_settings.REDIS_POOL_MAX_CONNECTIONS
        )
        self.client = Redis(
            connection_pool=redis_connection_pool
        )
        logger.info("Connected to redis!")

    async def disconnect(self):
        logger.info("Disconnecting Redis...")
        if self.client:
            await self.client.close()
            self.client = None
        logger.info("Redis disconnected!")

redis_manager = RedisClient()