from datetime import datetime
from app.core.correlation import get_correlation_id

def success_response(data):
    request_id = get_correlation_id()
    return {
        "status": "success",
        "request_id": request_id,
        "timestamp": datetime.utcnow().isoformat(),
        "data": data,
    }

def error_response(code, message):
    request_id = get_correlation_id()
    return {
        "status": "error",
        "request_id": request_id,
        "timestamp": datetime.now().isoformat(),
        "error": {"code": code, "message": message},
    }