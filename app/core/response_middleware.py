from __future__ import annotations

import json
from datetime import datetime


class StandardResponseMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        status_code = None
        headers = None
        body_chunks = []

        async def send_wrapper(message):
            nonlocal status_code, headers

            # Capture status & headers
            if message["type"] == "http.response.start":
                status_code = message["status"]
                headers = {
                    k.decode(): v.decode()
                    for k, v in message.get("headers", [])
                }
                return  # wait for body

            # Capture body
            if message["type"] == "http.response.body":
                body_chunks.append(message.get("body", b""))

                if not message.get("more_body", False):
                    full_body = b"".join(body_chunks)

                    # CRITICAL FIX — DO NOT WRAP ERRORS
                    print("status code is", status_code)
                    if status_code >= 400:
                        await send(
                            {
                                "type": "http.response.start",
                                "status": status_code,
                                "headers": [
                                    (k.encode(), v.encode())
                                    for k, v in headers.items()
                                ],
                            }
                        )
                        await send(
                            {
                                "type": "http.response.body",
                                "body": full_body,
                                "more_body": False,
                            }
                        )
                        return

                    # Only wrap successful JSON responses
                    content_type = headers.get("content-type", "")
                    if "application/json" in content_type:
                        try:
                            payload = json.loads(full_body)

                            # Prevent double wrapping
                            if not (
                                isinstance(payload, dict)
                                and "status" in payload
                            ):
                                wrapped = {
                                    "status": "success",
                                    "request_id": scope.get("state", {}).get(
                                        "request_id"
                                    ),
                                    "timestamp": datetime.isoformat(),
                                    "data": payload,
                                }

                                full_body = json.dumps(wrapped).encode()
                                headers.pop("content-length", None)

                        except Exception:
                            pass

                    # Send modified response
                    await send(
                        {
                            "type": "http.response.start",
                            "status": status_code,
                            "headers": [
                                (k.encode(), v.encode())
                                for k, v in headers.items()
                            ],
                        }
                    )

                    await send(
                        {
                            "type": "http.response.body",
                            "body": full_body,
                            "more_body": False,
                        }
                    )

                return

            await send(message)

        await self.app(scope, receive, send_wrapper)
