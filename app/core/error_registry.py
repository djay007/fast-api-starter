from enum import Enum


class ErrorCode(str, Enum):
    # General
    INTERNAL_ERROR = "GEN_001"
    VALIDATION_ERROR = "GEN_002"

    # Auth
    INVALID_TOKEN = "AUTH_001"
    UNAUTHORIZED = "AUTH_002"

    # User
    USER_NOT_FOUND = "USER_001"
    EMAIL_ALREADY_EXISTS = "USER_002"

    # Database
    DATABASE_ERROR = "DB_001"