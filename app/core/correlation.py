import contextvars

correlation_id_context = contextvars.ContextVar("correlation_id", default=None)

def set_correlation_id(request_id: str):
    correlation_id_context.set(request_id)

def get_correlation_id():
    return correlation_id_context.get()