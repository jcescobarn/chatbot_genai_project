import redis
from core.config import settings


class RedisClient:
    def __init__(self):
        self.client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)


    def get_client(self):
        return self.client

redis_client = RedisClient().get_client()