# Installation Guide

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- 4GB+ RAM
- 10GB+ disk space

## Installation Methods

### Method 1: Docker Compose (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/NickScherbakov/sentio-iot.git
cd sentio-iot
```

2. **Configure environment**
```bash
# Create environment file
cat > .env << EOF
JWT_SECRET_KEY=$(openssl rand -hex 32)
POSTGRES_PASSWORD=sentio
EOF
```

3. **Start services**
```bash
docker-compose up -d
```

4. **Verify installation**
```bash
docker-compose ps
```

All services should be running. Access the dashboard at http://localhost:3000

### Method 2: Manual Installation

#### API Server
```bash
cd api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8080
```

#### Dashboard
```bash
cd dashboard
npm install
npm run dev
```

#### Collectors
```bash
cd collectors
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Method 3: Kubernetes

Coming soon - Kubernetes manifests and Helm charts will be available.

## Post-Installation

### 1. Change Default Credentials
- Login to dashboard with `admin` / `admin`
- Navigate to Settings > Users
- Change the admin password

### 2. Configure Connectors
Edit `config/connectors.yml` to set up your device integrations

### 3. Set Up Alerts
Configure alert rules in the dashboard under Alerts section

## Verification

Check system health:
```bash
curl http://localhost:8080/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-09T08:00:00",
  "version": "1.0.0"
}
```

## Troubleshooting

### Services won't start
```bash
# Check logs
docker-compose logs

# Restart services
docker-compose restart
```

### Port conflicts
Edit `docker-compose.yml` to change port mappings

### Low memory
Reduce retention periods in `config/loki-config.yml` and `config/tempo-config.yml`
