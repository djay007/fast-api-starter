from __future__ import annotations

from pydantic import BaseModel


class Settings(BaseModel):
    ENV: str
    APP_NAME: str

    JWT_SECRET: str
    ENCRYPTION_KEY: str

    AWS_REGION: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    DDB_TABLE: str
    S3_BUCKET: str
    DDB_URL: str

    RATE_LIMIT_MAX: int
    RATE_LIMIT_WINDOW: int

    # Audit
    AUDIT_ENABLED: bool = True
    AUDIT_MAX_BODY_SIZE: int = 5000
