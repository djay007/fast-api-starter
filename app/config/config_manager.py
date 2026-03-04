import asyncio
from typing import Optional

import redis.asyncio as redis

from app.config.bootstrap_settings import bootstrap_settings
from app.config.runtime_settings import Settings


class AsyncConfigManager:
    def __init__(self):
        self.env = bootstrap_settings.ENV

        self.redis = redis.Redis(
            host=bootstrap_settings.VALKEY_HOST,
            port=bootstrap_settings.VALKEY_PORT,
            password=bootstrap_settings.VALKEY_PASSWORD,
            decode_responses=True,
        )

        self._settings: Optional[Settings] = None
        self._reload_lock = asyncio.Lock()

    async def load_config(self):
        key = f"app:config:{self.env}"
        data = await self.redis.hgetall(key)

        if not data:
            raise RuntimeError(f"No runtime config found for env={self.env}")

        new_settings = Settings(**data)

        # Atomic pointer swap (lock-free read)
        self._settings = new_settings
        print ("settings", self._settings)
        print("[ConfigManager] Runtime config loaded")

    def get_settings(self) -> Settings:
        if not self._settings:
            raise RuntimeError("Config not initialized")
        return self._settings

    async def start_listener(self):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe("app:config:reload")

        print("[ConfigManager] Listening for reload events...")

        async for message in pubsub.listen():
            if message["type"] != "message":
                continue

            if message["data"] == self.env:
                print("[ConfigManager] Reload event received")
                async with self._reload_lock:
                    await self.load_config()


config_manager = AsyncConfigManager()


def get_settings() -> Settings:
    return config_manager.get_settings()