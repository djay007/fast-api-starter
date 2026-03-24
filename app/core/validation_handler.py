from __future__ import annotations

from fastapi import Request
from fastapi.exceptions import RequestValidationError

from app.core.error_builder import build_error_response
from app.core.error_registry import ErrorCode


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    formatted_errors = []

    for err in exc.errors():
        formatted_errors.append(
            {
                "field": ".".join(map(str, err["loc"])),
                "message": err["msg"],
                "type": err["type"],
            }
        )

    return build_error_response(
        request,
        status_code=422,
        error_code=ErrorCode.VALIDATION_ERROR,
        message="Validation failed",
        details={"fields": formatted_errors},
    )
