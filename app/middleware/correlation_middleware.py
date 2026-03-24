from __future__ import annotations

import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.correlation import set_correlation_id


class CorrelationIdMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        # store in context
        set_correlation_id(request_id)

        # store in request
        request.state.request_id = request_id

        response = await call_next(request)

        response.headers["X-Request-ID"] = request_id

        return response
