from __future__ import annotations

from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.error_codes import ERROR_CODES
from app.core.response import error_response
from app.core.security import verify_token

PUBLIC_ROUTES = {
    "/health",
    "/docs",
    "/openapi.json",
    "/redoc",
    "/api/v1/sample",
}


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # import pdb; pdb.set_trace
        # Skip auth for public routes
        print(request.url.path)
        print(PUBLIC_ROUTES)
        print("Request Path:", request.url.path)
        if request.url.path in PUBLIC_ROUTES:
            print("Public route condition is true")
            return await call_next(request)

        # Skip auth in dev environment (optional but recommended)
        print("Protected route")
        token = request.headers.get("Authorization")

        if not token:
            return JSONResponse(
                status_code=401,
                content=error_response(
                    "AUTH_001",
                    ERROR_CODES["AUTH_001"],
                    "N/A",
                ),
            )

        decoded = verify_token(token.replace("Bearer ", ""))

        if not decoded:
            return JSONResponse(
                status_code=401,
                content=error_response(
                    "AUTH_002",
                    ERROR_CODES["AUTH_001"],
                    "N/A",
                ),
            )

        return await call_next(request)
