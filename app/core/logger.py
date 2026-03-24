from __future__ import annotations

import json
import logging
from datetime import datetime

from app.core.correlation import get_correlation_id

SENSITIVE_FIELDS = {"password", "ssn", "credit_card", "token", "authorization"}


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "service": "fastapi-aws-enterprise",  # microservice name
            "level": record.levelname,
            "message": record.getMessage(),
        }

        # Include structured extra data if provided
        extra_data = getattr(record, "extra_data", None)
        if isinstance(extra_data, dict):
            log_data.update(self._sanitize(extra_data))

        return json.dumps(log_data)

    def _sanitize(self, data: dict):
        sanitized = {}
        for key, value in data.items():
            if key.lower() in SENSITIVE_FIELDS:
                sanitized[key] = "[REDACTED]"
            else:
                sanitized[key] = value
        return sanitized


class CorrelationIdFilter(logging.Filter):

    def filter(self, record):
        record.request_id = get_correlation_id()
        return True


def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    handler.addFilter(CorrelationIdFilter())

    app_logger = logging.getLogger("app")
    app_logger.setLevel(logging.INFO)
    app_logger.handlers.clear()
    app_logger.addHandler(handler)
    app_logger.propagate = False


# 👇 GLOBAL LOGGER INSTANCE (Application Level)
logger = logging.getLogger("app")
