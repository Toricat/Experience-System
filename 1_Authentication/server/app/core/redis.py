import redis.asyncio as redis
from core.config import settings

class RedisClient:
    _instance = None

    @staticmethod
    async def get_instance():
        """Khởi tạo Redis client với Redis asyncio nếu chưa có."""
        if RedisClient._instance is None:
            RedisClient._instance = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=0,
                decode_responses=True,  
                max_connections=10,     
            )
        return RedisClient._instance

async def get_redis_client():
    """Trả về instance của Redis (bất đồng bộ)."""
    return await RedisClient.get_instance()
