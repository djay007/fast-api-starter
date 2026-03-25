#!/bin/sh

echo "Starting FastAPI with Gunicorn..."

exec gunicorn app.main:app \
    -k uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --workers 1 \
    --timeout 120
