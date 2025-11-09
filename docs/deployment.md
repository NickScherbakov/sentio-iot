# Deployment Guide

This guide covers various deployment scenarios for Sentio IoT.

## Table of Contents

1. [Docker Compose (Development)](#docker-compose-development)
2. [Docker Compose (Production)](#docker-compose-production)
3. [Cloud Deployment](#cloud-deployment)
4. [On-Premises Deployment](#on-premises-deployment)
5. [High Availability Setup](#high-availability-setup)

## Docker Compose (Development)

### Quick Start
```bash
git clone https://github.com/NickScherbakov/sentio-iot.git
cd sentio-iot
docker-compose up -d
```

Access at:
- Dashboard: http://localhost:3000
- API: http://localhost:8080
- VictoriaMetrics: http://localhost:8428

## Docker Compose (Production)

### 1. Prepare Environment

```bash
# Create production environment file
cat > .env << EOF
# Security
JWT_SECRET_KEY=$(openssl rand -hex 32)

# Database
POSTGRES_PASSWORD=$(openssl rand -hex 16)
DATABASE_URL=postgresql://sentio:${POSTGRES_PASSWORD}@postgres:5432/sentio

# Optional: External URLs for cloud deployment
EXTERNAL_API_URL=https://api.yourdomain.com
EXTERNAL_DASHBOARD_URL=https://dashboard.yourdomain.com
EOF
```

### 2. Update docker-compose.yml

```yaml
# Add resource limits
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
    restart: always
```

### 3. Set Up SSL/TLS

```bash
# Generate self-signed certificates (for testing)
mkdir -p certs
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout certs/key.pem \
  -out certs/cert.pem

# For production, use Let's Encrypt certificates
```

### 4. Configure Reverse Proxy (Nginx)

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://localhost:8080/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws {
        proxy_pass http://localhost:8080/ws;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 5. Start Services

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Cloud Deployment

### AWS (ECS/Fargate)

1. **Build and push Docker images**
```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

# Build and tag images
docker-compose build
docker tag sentio-api:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/sentio-api:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/sentio-api:latest
```

2. **Create ECS Task Definition**
```json
{
  "family": "sentio-iot",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "api",
      "image": "YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/sentio-api:latest",
      "portMappings": [
        {
          "containerPort": 8080,
          "protocol": "tcp"
        }
      ]
    }
  ]
}
```

3. **Deploy with terraform** (optional)
```hcl
# See terraform/ directory for complete configuration
```

### Google Cloud (GKE)

1. **Create GKE cluster**
```bash
gcloud container clusters create sentio-cluster \
  --num-nodes=3 \
  --machine-type=n1-standard-2 \
  --region=us-central1
```

2. **Deploy with kubectl** (Kubernetes manifests coming soon)

### Azure (AKS)

1. **Create AKS cluster**
```bash
az aks create \
  --resource-group sentio-rg \
  --name sentio-cluster \
  --node-count 3 \
  --node-vm-size Standard_D2s_v3
```

2. **Deploy with helm** (Helm charts coming soon)

### DigitalOcean

1. **Create Droplet**
```bash
doctl compute droplet create sentio \
  --size s-2vcpu-4gb \
  --image docker-20-04 \
  --region nyc3
```

2. **SSH and deploy**
```bash
ssh root@YOUR_DROPLET_IP
git clone https://github.com/NickScherbakov/sentio-iot.git
cd sentio-iot
docker-compose up -d
```

## On-Premises Deployment

### Single Server

**System Requirements:**
- 8 CPU cores
- 16GB RAM
- 500GB SSD
- Ubuntu 20.04+ or RHEL 8+

**Installation:**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Deploy Sentio IoT
git clone https://github.com/NickScherbakov/sentio-iot.git
cd sentio-iot
docker-compose up -d
```

### High Availability Setup

**Architecture:**
```
                    Load Balancer
                    /     |     \
                   /      |      \
              API-1    API-2    API-3
                   \      |      /
                    \     |     /
                  PostgreSQL (Primary + Replica)
                  VictoriaMetrics Cluster
                  Redis Cluster
```

**docker-compose.ha.yml:**
```yaml
version: '3.8'

services:
  api:
    deploy:
      replicas: 3
      
  postgres:
    image: postgres:15-alpine
    command: postgres -c 'max_connections=200'
    
  postgres-replica:
    image: postgres:15-alpine
    environment:
      - POSTGRES_MASTER_HOST=postgres
      
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes --cluster-enabled yes
```

**Deploy:**
```bash
docker-compose -f docker-compose.yml -f docker-compose.ha.yml up -d --scale api=3
```

## Monitoring Deployment

### Health Checks
```bash
# Check all services
curl http://localhost:8080/health
curl http://localhost:8428/health
curl http://localhost:3100/ready

# Check Docker containers
docker-compose ps

# Check logs
docker-compose logs -f api
```

### Prometheus Monitoring

Add Prometheus to monitor Sentio IoT:
```yaml
prometheus:
  image: prom/prometheus
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
  ports:
    - "9090:9090"
```

## Backup and Recovery

### Backup Script
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# Backup PostgreSQL
docker exec sentio-postgres pg_dump -U sentio sentio > $BACKUP_DIR/postgres_$DATE.sql

# Backup configurations
tar -czf $BACKUP_DIR/config_$DATE.tar.gz config/

# Backup VictoriaMetrics data
docker exec sentio-victoriametrics tar -czf - /victoria-metrics-data > $BACKUP_DIR/metrics_$DATE.tar.gz
```

### Restore
```bash
# Restore PostgreSQL
cat postgres_backup.sql | docker exec -i sentio-postgres psql -U sentio

# Restore configurations
tar -xzf config_backup.tar.gz
```

## Scaling Considerations

### Vertical Scaling
- Increase resources in docker-compose.yml
- Monitor with `docker stats`

### Horizontal Scaling
- Scale collectors: `docker-compose up -d --scale collectors=3`
- Scale API: Use load balancer with multiple instances
- Use VictoriaMetrics cluster for metrics storage

### Storage Scaling
- Mount external volumes for data persistence
- Use S3/GCS for long-term storage
- Configure retention policies

## Troubleshooting

### Services won't start
```bash
docker-compose logs
docker-compose ps
```

### High resource usage
```bash
docker stats
# Adjust resource limits in docker-compose.yml
```

### Network issues
```bash
docker network inspect sentio-network
```

## Security Checklist

- [ ] Change default credentials
- [ ] Enable TLS/SSL
- [ ] Configure firewall rules
- [ ] Set up authentication
- [ ] Enable audit logging
- [ ] Regular security updates
- [ ] Backup encryption
- [ ] Network segmentation

## Post-Deployment

1. Verify all services are running
2. Configure connectors for your devices
3. Set up alerts and notifications
4. Configure backup schedule
5. Set up monitoring and alerting
6. Document your specific configuration
