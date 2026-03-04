from datetime import datetime
from fastapi.responses import JSONResponse
from app.core.error_registry import ErrorCode


def build_error_response(
    request,
    status_code: int,
    error_code: ErrorCode,
    message: str,
    details: dict | None = None,
):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "request_id": getattr(request.state, "request_id", None),
            "timestamp": datetime.utcnow().isoformat(),
            "error": {
                "code": error_code.value,
                "message": message,
                "details": details,
            },
        },
    )