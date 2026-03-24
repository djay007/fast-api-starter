from __future__ import annotations

import redis.asyncio as redis

from app.config.bootstrap_settings import bootstrap_settings

_redis_client = None


def get_redis_client():
    global _redis_client

    if _redis_client is None:
        _redis_client = redis.Redis(
            host=bootstrap_settings.VALKEY_HOST,
            port=bootstrap_settings.VALKEY_PORT,
            password=bootstrap_settings.VALKEY_PASSWORD,
            decode_responses=True,
        )

    return _redis_client
