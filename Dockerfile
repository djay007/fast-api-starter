FROM python:3.12-slim

WORKDIR /app

# Install minimal system deps (safe fallback)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# VERY IMPORTANT
RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .
RUN pip install --no-cache-dir --only-binary=:all: -r requirements.txt
RUN pip install pydantic[email]
COPY . .
RUN useradd -m appuser
USER appuser
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
