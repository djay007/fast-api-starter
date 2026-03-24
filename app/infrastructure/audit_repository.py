from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor

import boto3

from app.config.config_manager import get_settings

executor = ThreadPoolExecutor(max_workers=5)

_cached_config_signature = None
_cached_table = None


def get_dynamodb_table():
    global _cached_config_signature
    global _cached_table

    settings = get_settings()

    signature = (
        settings.AWS_REGION,
        settings.AWS_ACCESS_KEY_ID,
        settings.AWS_SECRET_ACCESS_KEY,
        settings.DDB_TABLE,
        settings.DDB_URL,
    )

    if signature != _cached_config_signature:
        if settings.DDB_URL:
            dynamodb = boto3.resource(
                "dynamodb",
                region_name=settings.AWS_REGION,
                endpoint_url=settings.DDB_URL,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )
        else:
            dynamodb = boto3.resource(
                "dynamodb",
                region_name=settings.AWS_REGION,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )

        _cached_table = dynamodb.Table(settings.DDB_TABLE)
        _cached_config_signature = signature

    return _cached_table


async def save_audit_record(record: dict):
    table = get_dynamodb_table()

    loop = asyncio.get_running_loop()
    await loop.run_in_executor(
        executor,
        lambda: table.put_item(Item=record),
    )
