from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.config.config_manager import get_settings

ALGORITHM = "HS256"


def generate_token(user_id: str, expires_minutes: int = 60) -> str:
    settings = get_settings()
    expire = datetime.now() + timedelta(minutes=expires_minutes)

    payload = {
        "sub": user_id,
        "exp": expire,
        "iat": datetime.now(),
    }

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=ALGORITHM)


def verify_token(token: str) -> dict | None:
    try:
        settings = get_settings()
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[ALGORITHM],
        )
        return payload
    except JWTError:
        return None     