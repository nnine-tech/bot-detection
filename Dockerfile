# ------------------------
# Stage 1: Base Image
# ------------------------
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies (if needed for pandas/numpy/scikit-learn)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc && \
    rm -rf /var/lib/apt/lists/*

# ------------------------
# Stage 2: Install Python deps
# ------------------------
# Copy only requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ------------------------
# Stage 3: Copy Application Code
# ------------------------
COPY . .

# Expose FastAPI port
EXPOSE 8000

# ------------------------
# Stage 4: Start App
# ------------------------
# Default command → run FastAPI server
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
