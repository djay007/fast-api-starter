# Enterprise Ready FastAPI Starter

## Features
- Postgres Connectivity using sql-alchemy
- Using valkey for configuation management
- Real Encryption/Decryption Middleware (Fernet AES)
- JWT Authentication/ Authorization Middleware
- Redis-based Rate Limiting
- Repositories: DB access only.
  Services: Business rules.
  Router: HTTP only.
  Client → Router → Service → DB → Service → Router → Response
- DynamoDB Audit Logging to store request and response (Large Response Offload to S3)
- Pydantic Validation
- Structured Logging with PII / Secret Redaction
- Standardized Success/Error Responses
- Enterprise grade folder structure
- Ruff + Black + MyPy
- Bandit, Safety, Semgrep
- Production Dockerfile


## Required Environment Variables

export REDIS_HOST=localhost
export REDIS_PORT=6379
export JWT_SECRET=your_secret
export ENCRYPTION_KEY=your_fernet_key
export DDB_TABLE=your_dynamodb_table
export S3_BUCKET=your_bucket_name

## Run

pip install -r requirements.txt
uvicorn app.main:app --reload

## Developer Guidelines

- Never hardcode credentials
- Always use Pydantic schemas
- Do not log sensitive fields
- Add new error codes in error_codes.py
- Follow structured logging
- Write unit tests for new endpoints

## Test Coverage

Run tests with coverage:

    pytest

Coverage reports:
- Terminal summary
- HTML report generated in `htmlcov/`

To open HTML report:

    open htmlcov/index.html   # macOS
    xdg-open htmlcov/index.html  # Linux
