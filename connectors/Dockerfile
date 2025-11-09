FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for industrial protocols
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 sentio && chown -R sentio:sentio /app
USER sentio

# Run the connectors
CMD ["python", "main.py"]
