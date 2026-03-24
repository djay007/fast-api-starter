from __future__ import annotations

import contextvars

correlation_id_context: contextvars.ContextVar[str | None] = (
    contextvars.ContextVar(
        "correlation_id",
        default=None,
    )
)


def set_correlation_id(request_id: str) -> None:
    correlation_id_context.set(request_id)


def get_correlation_id() -> str | None:
    return correlation_id_context.get()
