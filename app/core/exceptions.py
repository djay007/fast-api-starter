from __future__ import annotations

from datetime import datetime

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.core.error_builder import build_error_response
from app.core.error_codes import ERROR_CODES
from app.core.error_registry import ErrorCode


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Database error occurred",
        },
    )


async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error",
        },
    )


def error_response(code: str, request_id: str):
    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "request_id": request_id,
            "timestamp": datetime.now().isoformat(),
            "error": {
                "code": code,
                "message": ERROR_CODES.get(code),
            },
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 409:
        return build_error_response(
            request,
            status_code=409,
            error_code=ErrorCode.EMAIL_ALREADY_EXISTS,
            message=exc.detail,
        )

    return build_error_response(
        request,
        status_code=exc.status_code,
        error_code=ErrorCode.INTERNAL_ERROR,
        message=exc.detail,
    )
