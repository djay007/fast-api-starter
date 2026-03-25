
# FastAPI Enterprise Starter

Production-ready **FastAPI backend framework** designed for enterprise-grade systems such as fintech, banking, and high-scale backend services.

This framework includes:
- Clean Architecture
- Auth Middleware
- Audit Middleware
- Correlation ID tracing
- Runtime & Bootstrap configuration separation
- Standard API response format
- Centralized logging
- Redis & PostgreSQL integration
- AWS-ready deployment
- Docker & CI/CD support

---

# Table of Contents

1. Project Overview
2. Developer Onboarding Guide
3. Project Architecture
4. Folder Structure
5. Configuration Management
6. Middleware Layer
7. API Design Standards
8. Example: Creating an API
9. Request Lifecycle
10. Architecture Diagram
11. Sequence Diagram (API Request Flow)
12. Deployment Architecture
13. Docker Setup
14. CI/CD Pipeline
15. Running the Application
16. Testing
17. Security Features
18. Developer Best Practices

---

# Project Overview

This repository provides a **production-grade FastAPI starter template** used for building scalable backend services.

Key capabilities:

- Enterprise architecture
- Middleware driven request processing
- Secure configuration loading
- Observability (correlation ID + logging)
- Audit trail support
- Authentication layer
- AWS cloud ready deployment

---

# Developer Onboarding Guide

## Prerequisites

Required tools:

| Tool | Version |
|-----|--------|
Python | 3.11+ |
Docker | Latest |
Git | Latest |
Redis | 6+ |
PostgreSQL | 13+ |

Check Python version:

```
python --version
```

---

## Clone Repository

```
git clone <repository-url>
cd fastapi-enterprise
```

---

## Create Virtual Environment

```
python -m venv venv
```

Activate environment

Linux / Mac

```
source venv/bin/activate
```

Windows

```
venv\Scripts\activate
```

---

## Install Dependencies and Run application

```
pip install -r requirements.txt
chmod +x start.sh
start.sh

```

---

## Install Dependencies related to Precommit hook

```
pip install -r requirements-dev.txt
pip install pre-commit
pre-commit --version
pre-commit clean
pre-commit install
pre-commit run --all-files
```

---

## Configure Environment Variables

Create `.env`

Example:

```
APP_ENV=dev
APP_NAME=fastapi-enterprise
AWS_REGION=ap-south-1

REDIS_HOST=localhost
REDIS_PORT=6379

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=sample
POSTGRES_USER=user
POSTGRES_PASSWORD=password
```

---

# Project Architecture

The system follows **Clean Architecture**.

```
Client
  │
  ▼
Middleware Layer
  │
  ▼
API Router
  │
  ▼
Service Layer
  │
  ▼
Repository Layer
  │
  ▼
Database / External Services
```

---

# Folder Structure

```
app
├── api
│   └── v1
│       └── router
│
├── core
│   ├── config
│   │   ├── bootstrap_config.py
│   │   └── runtime_config.py
│   │
│   ├── logging.py
│   ├── correlation.py
│   └── responses.py
│
├── middleware
│   ├── correlation_middleware.py
│   ├── auth_middleware.py
│   ├── audit_middleware.py
│   ├── logging_middleware.py
│   └── encryption_middleware.py
│
├── services
├── repositories
├── models
├── schemas
├── utils
│
└── main.py
```

---

# Configuration Management

Configuration is separated into **Bootstrap Config** and **Runtime Config**.

## Bootstrap Configuration

Loaded during application startup.

Examples:

- application environment
- AWS region
- secret path

Location:

```
app/core/config/bootstrap_config.py
```

---

## Runtime Configuration

Loaded after bootstrap initialization.

Examples:

- database credentials
- redis configuration
- encryption keys

Location:

```
app/core/config/runtime_config.py
```

---

# Middleware Layer

Middleware intercepts every request before it reaches the router.

Execution order:

```
1. Correlation Middleware
2. Logging Middleware
3. Auth Middleware
4. Audit Middleware
5. Encryption Middleware
```

Responsibilities:

| Middleware | Purpose |
|-----------|--------|
Correlation | Generate request ID |
Logging | Log request and response |
Auth | Validate token |
Audit | Store audit logs |
Encryption | Encrypt/decrypt payloads |

---

# API Design Standards

## URL Naming

Correct

```
/api/v1/users
/api/v1/users/{id}
```

Incorrect

```
/api/v1/getUsers
```

---

## HTTP Methods

| Method | Usage |
|------|------|
GET | Retrieve resource |
POST | Create resource |
PUT | Update resource |
PATCH | Partial update |
DELETE | Remove resource |

---

## Status Codes

| Code | Meaning |
|-----|--------|
200 | Success |
201 | Created |
400 | Bad request |
401 | Unauthorized |
403 | Forbidden |
404 | Not found |
422 | Validation error |
500 | Internal server error |

---

## Standard Response Format

Success

```
{
 "status": "success",
 "request_id": "uuid",
 "data": {}
}
```

Error

```
{
 "status": "error",
 "request_id": "uuid",
 "message": "Invalid request"
}
```

---

# Example: Creating an API

Example endpoint:

```
POST /api/v1/users
```

Router:

```
@router.post("/users")
async def create_user(payload: CreateUserRequest):
    user = await user_service.create_user(payload.dict())
    return success_response(data=user)
```

Service:

```
class UserService:

    async def create_user(self, data):
        return await user_repository.create_user(data)
```

Repository:

```
class UserRepository:

    async def create_user(self, data):
        return {"id":1,"name":data["name"]}
```

---

# API Request Lifecycle

```
Client Request
      │
      ▼
Correlation Middleware
      │
Logging Middleware
      │
Auth Middleware
      │
Audit Middleware
      │
Encryption Middleware
      │
Router
      │
Service Layer
      │
Repository Layer
      │
Database
      │
Response Builder
      │
Client Response
```

---

# Architecture Diagram

```
Client
  │
  ▼
AWS Load Balancer
  │
  ▼
FastAPI Service (Docker)
  │
 ┌─────────────┴─────────────┐
 ▼                           ▼
Redis Cache              PostgreSQL
 │                           │
 ▼                           ▼
ElastiCache                 AWS RDS
```

---

# Sequence Diagram (API Request Flow)

```
Client
 │
 ▼
API Gateway
 │
 ▼
FastAPI Application
 │
 ▼
Correlation Middleware
 │
 ▼
Logging Middleware
 │
 ▼
Auth Middleware
 │
 ▼
Audit Middleware
 │
 ▼
Encryption Middleware
 │
 ▼
Router
 │
 ▼
Service
 │
 ▼
Repository
 │
 ▼
Database
 │
 ▼
Response
```

---

# Deployment Architecture

```
Internet
   │
   ▼
AWS ALB / API Gateway
   │
   ▼
ECS / Kubernetes
   │
   ▼
FastAPI Containers
   │
 ┌─────────────┴─────────────┐
 ▼                           ▼
Redis                     PostgreSQL
 │                           │
 ▼                           ▼
ElastiCache                RDS
```

---

# Docker Setup

Example Dockerfile

```
FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
```

---

# CI/CD Pipeline

```
Code Push
   │
   ▼
Install Dependencies
   │
   ▼
Run Tests
   │
   ▼
Lint & Security Scan
   │
   ▼
Build Docker Image
   │
   ▼
Push to Container Registry
   │
   ▼
Deploy to ECS / Kubernetes
```

---

# Running the Application

Start server

```
uvicorn app.main:app --reload
```

Swagger documentation

```
http://localhost:8000/docs
```

---

# Testing

Run tests

```
pytest
```

Run coverage

```
pytest --cov=app
```

---

# Security Features

Implemented controls:

- Authentication middleware
- Audit logging
- Encryption middleware
- Secrets manager integration
- Correlation ID tracing
- Centralized logging

---

# Developer Best Practices

- Keep routers thin
- Place business logic in services
- Use repositories for database operations
- Follow API design standards
- Use centralized logging
- Write async code for I/O operations
