from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from cryptography.fernet import Fernet
import os

key = os.getenv("ENCRYPTION_KEY")
fernet = Fernet(key) if key else None


class EncryptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):

        # ---- Decrypt Request ----
        if fernet:
            body = await request.body()
            if body:
                try:
                    decrypted = fernet.decrypt(body)
                    request._body = decrypted
                except Exception:
                    # If not encrypted, ignore (dev mode safe)
                    pass

        # ---- Call endpoint ----
        response = await call_next(request)

        # If no encryption configured, return directly
        if not fernet:
            return response

        # ---- Capture Response Body Safely ----
        response_body = b""

        if hasattr(response, "body_iterator"):
            body_chunks = []
            async for chunk in response.body_iterator:
                body_chunks.append(chunk)

            response_body = b"".join(body_chunks)

            # Encrypt response
            encrypted_body = fernet.encrypt(response_body)

            # Rebuild response
            response = Response(
                content=encrypted_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )

        elif hasattr(response, "body"):
            response_body = response.body or b""
            encrypted_body = fernet.encrypt(response_body)

            response = Response(
                content=encrypted_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )

        return response