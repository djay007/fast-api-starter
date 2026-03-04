import uuid
import asyncio
from datetime import datetime
from starlette.types import ASGIApp, Scope, Receive, Send

from app.config.config_manager import get_settings
from app.infrastructure.audit_repository import save_audit_record


class AuditMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        settings = get_settings()
        print ("AUDIT flag", settings.AUDIT_ENABLED)
        if not settings.AUDIT_ENABLED:
            await self.app(scope, receive, send)
            return

        request_id = str(uuid.uuid4())
        scope["request_id"] = request_id

        request_body_chunks = []
        response_body_chunks = []
        status_code = None

        # ---- Wrap receive to capture request body ----
        async def receive_wrapper():
            message = await receive()

            if message["type"] == "http.request":
                body = message.get("body", b"")
                if body:
                    request_body_chunks.append(body)

            return message

        # ---- Wrap send to capture response body ----
        async def send_wrapper(message):
            nonlocal status_code

            if message["type"] == "http.response.start":
                status_code = message["status"]

            if message["type"] == "http.response.body":
                body = message.get("body", b"")
                if body:
                    response_body_chunks.append(body)

            await send(message)

        # ---- Call downstream app ----
        await self.app(scope, receive_wrapper, send_wrapper)

        # ---- After response sent ----
        request_body = b"".join(request_body_chunks)
        response_body = b"".join(response_body_chunks)

        # Limit response size
        if len(response_body) > settings.AUDIT_MAX_BODY_SIZE:
            response_body = b"[BODY_TOO_LARGE]"

        audit_record = {
            "request_id": request_id,
            "endpoint": scope["path"],
            "method": scope["method"],
            "status_code": status_code,
            "payload": request_body.decode(errors="ignore"),
            "response": response_body.decode(errors="ignore"),
            "timestamp": datetime.now().isoformat(),
            "ip": scope.get("client")[0] if scope.get("client") else None,
        }

        # 🔥 Non-blocking save
        asyncio.create_task(save_audit_record(audit_record))