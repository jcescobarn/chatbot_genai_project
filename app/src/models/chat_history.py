from typing import List
from core.redis_client import redis_client


class ChatHistory:
    def __init__(self, user_id: str):
        self.key = f"chat_history:{user_id}:"

    def get(self) -> List[str]:
        return redis_client.lrange(self.key, 0, -1)

    def append(self, message: str) -> None:
        redis_client.rpush(self.key, message)