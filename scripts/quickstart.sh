#!/bin/bash

# Sentio IoT Quick Start Script
# This script helps you get Sentio IoT up and running quickly

set -e

echo "====================================="
echo "  Sentio IoT Quick Start"
echo "====================================="
echo ""

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check for Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    if [ -f .env.example ]; then
        cp .env.example .env
    else
        cat > .env << EOF
# Security
JWT_SECRET_KEY=$(openssl rand -hex 32 2>/dev/null || echo "change-me-in-production-$(date +%s)")

# Database
POSTGRES_PASSWORD=sentio

# CORS Origins (add your domains)
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
EOF
    fi
    echo "✅ Created .env file"
else
    echo "✅ .env file already exists"
fi
echo ""

# Create data directories
echo "📁 Creating data directories..."
mkdir -p data/{victoriametrics,loki,tempo,postgres,redis}
mkdir -p models
mkdir -p certs
echo "✅ Data directories created"
echo ""

# Pull images
echo "📦 Pulling Docker images (this may take a while)..."
docker-compose pull
echo "✅ Images pulled"
echo ""

# Start services
echo "🚀 Starting Sentio IoT services..."
docker-compose up -d
echo "✅ Services started"
echo ""

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo "🔍 Checking service health..."
services=("api" "victoriametrics" "loki" "tempo" "postgres" "redis" "collectors" "connectors" "ai-engine" "dashboard")
all_healthy=true

for service in "${services[@]}"; do
    if docker-compose ps | grep "$service" | grep -q "Up"; then
        echo "  ✅ $service is running"
    else
        echo "  ❌ $service is not running"
        all_healthy=false
    fi
done
echo ""

if [ "$all_healthy" = true ]; then
    echo "====================================="
    echo "  🎉 Sentio IoT is ready!"
    echo "====================================="
    echo ""
    echo "Access the platform:"
    echo "  Dashboard:        http://localhost:3000"
    echo "  API:              http://localhost:8080"
    echo "  VictoriaMetrics:  http://localhost:8428"
    echo ""
    echo "Default credentials:"
    echo "  Username: admin"
    echo "  Password: admin"
    echo ""
    echo "Next steps:"
    echo "  1. Open http://localhost:3000 in your browser"
    echo "  2. Login with the default credentials"
    echo "  3. Configure your device connectors in config/connectors.yml"
    echo "  4. Check the documentation in docs/"
    echo ""
    echo "To stop Sentio IoT:"
    echo "  docker-compose down"
    echo ""
    echo "To view logs:"
    echo "  docker-compose logs -f"
    echo ""
else
    echo "====================================="
    echo "  ⚠️  Some services failed to start"
    echo "====================================="
    echo ""
    echo "Check logs with:"
    echo "  docker-compose logs"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Ensure ports 3000, 8080, 8428, 3100, 3200, 5432, 6379 are available"
    echo "  2. Check Docker resources (CPU, memory)"
    echo "  3. Review the logs for specific error messages"
fi
