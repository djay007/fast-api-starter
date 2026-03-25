# Developer Onboarding Guide

## Prerequisites

Required tools:

| Tool | Version |
|-----|--------|
Python | 3.12+ |
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

## 📁 Project Structure

. ├── app/ ├── Dockerfile ├── docker-compose.yml ├── requirements.txt
├── start.sh ├── .env └── README.md


## 🐳 Run

docker compose up -d --build

## 🛑 Stop

docker compose down

## 🔄 Rebuild

docker compose build --no-cache


## Rebuild and Restart

docker compose down
docker compose build
docker compose up -d


## Remove old Container

docker ps -a
docker rm -f <container_id>

## Useful Debug Commands

docker exec -it <container_id> sh

## Check environment variables:

docker exec -it <container_id> env

## 🌐 Access

http://localhost:8000/health
