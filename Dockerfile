# ------------------------
# Stage 1: Base Image
# ------------------------
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc curl && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# ------------------------
# Stage 2: Install Python deps
# ------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ------------------------
# Stage 3: Copy Application Code
# ------------------------
COPY . .

EXPOSE 8003

# ------------------------
# Stage 4: Start App
# ------------------------
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8003"]
