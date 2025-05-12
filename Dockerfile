# syntax=docker/dockerfile:1

FROM python:3.10-slim

# Install system deps
RUN apt-get update && apt-get install -y \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy your sample CSV into /app/data/
RUN mkdir -p /app/data
COPY data.csv /app/data/data.csv

# Copy API entrypoint to /app
COPY src/app_api.py .
# Also copy your rag package
COPY src/rag/ ./rag/

EXPOSE 8000

CMD ["uvicorn", "app_api:app", "--host", "0.0.0.0", "--port", "8000"]
