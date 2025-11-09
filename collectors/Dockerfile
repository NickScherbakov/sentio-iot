FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 sentio && chown -R sentio:sentio /app
USER sentio

# Expose collector port
EXPOSE 8081

# Run the collector
CMD ["python", "main.py"]
