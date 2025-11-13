# Quick Reference

Essential commands and configurations for Sentio IoT.

## 🚀 Quick Start

```bash
# Clone and start
git clone https://github.com/NickScherbakov/sentio-iot.git
cd sentio-iot
docker-compose up -d

# Access
open http://localhost:3000
# Login: admin / admin
```

## 📦 Docker Commands

### Basic Operations
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose stop

# Restart all services
docker-compose restart

# View status
docker-compose ps

# Remove everything
docker-compose down -v
```

### Logs
```bash
# View all logs
docker-compose logs

# Follow logs
docker-compose logs -f

# Specific service
docker-compose logs -f api

# Last 100 lines
docker-compose logs --tail=100
```

### Service Management
```bash
# Restart specific service
docker-compose restart api

# Rebuild service
docker-compose up -d --build api

# Scale service
docker-compose up -d --scale collectors=3
```

## 🔍 Health Checks

```bash
# API Server
curl http://localhost:8080/health

# VictoriaMetrics
curl http://localhost:8428/health

# Loki
curl http://localhost:3100/ready

# All services status
docker-compose ps
```

## 📊 Accessing Services

| Service | URL | Description |
|---------|-----|-------------|
| Dashboard | http://localhost:3000 | Web UI |
| API | http://localhost:8080 | REST API |
| API Docs | http://localhost:8080/docs | Swagger UI |
| VictoriaMetrics | http://localhost:8428 | Metrics DB |
| Loki | http://localhost:3100 | Logs DB |
| Tempo | http://localhost:3200 | Traces DB |
| PostgreSQL | localhost:5432 | Metadata DB |
| Redis | localhost:6379 | Cache |

## 🔐 Authentication

### Login
```bash
curl -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'
```

### Use Token
```bash
TOKEN="your-jwt-token"

curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8080/api/v1/devices
```

## 📈 Query Metrics

### PromQL Examples
```bash
# Current values
curl 'http://localhost:8428/api/v1/query?query=device_temperature'

# Time range
curl 'http://localhost:8428/api/v1/query_range?query=device_temperature&start=2024-01-01T00:00:00Z&end=2024-01-02T00:00:00Z&step=5m'

# Aggregations
curl 'http://localhost:8428/api/v1/query?query=avg(device_temperature)'
```

### LogQL Examples
```bash
# Recent logs
curl -G 'http://localhost:3100/loki/api/v1/query_range' \
  --data-urlencode 'query={job="sentio"}'

# Filter by level
curl -G 'http://localhost:3100/loki/api/v1/query_range' \
  --data-urlencode 'query={job="sentio"} |= "error"'
```

## ⚙️ Configuration Files

```
sentio-iot/
├── .env                          # Environment variables
├── docker-compose.yml            # Service definitions
├── config/
│   ├── connectors.yml           # Device connectors
│   ├── loki-config.yml          # Loki configuration
│   └── tempo-config.yml         # Tempo configuration
```

### Key Environment Variables
```bash
# .env
DATABASE_URL=postgresql://sentio:sentio@postgres:5432/sentio
REDIS_URL=redis://redis:6379
JWT_SECRET_KEY=change-me-in-production
CORS_ORIGINS=http://localhost:3000
```

## 🔌 Connector Examples

### Home Assistant
```yaml
# config/connectors.yml
home_assistant:
  enabled: true
  base_url: "http://homeassistant.local:8123"
  token: "your-long-lived-token"
  poll_interval: 30
```

### Modbus
```yaml
modbus:
  enabled: true
  devices:
    - name: "plc_1"
      host: "192.168.1.10"
      port: 502
      slave_id: 1
      poll_interval: 5
```

### Zigbee (MQTT)
```yaml
zigbee:
  enabled: true
  mqtt_broker: "mqtt://192.168.1.100:1883"
  base_topic: "zigbee2mqtt"
```

## 🐛 Troubleshooting

### Services Won't Start
```bash
# Check logs
docker-compose logs

# Check ports
sudo lsof -i :8080

# Restart
docker-compose restart
```

### No Data in Dashboard
```bash
# Check collectors
docker-compose logs collectors

# Test connectivity
docker-compose exec collectors ping victoriametrics

# Verify config
cat config/connectors.yml
```

### API Returns 401
```bash
# Get new token
curl -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'
```

### High Memory Usage
```bash
# Check usage
docker stats

# Reduce retention
# Edit docker-compose.yml
command:
  - "--retentionPeriod=1"  # months
```

## 📦 Backup & Restore

### Backup
```bash
# Stop services
docker-compose stop

# Backup data
tar -czf backup-$(date +%Y%m%d).tar.gz data/

# Start services
docker-compose start
```

### Restore
```bash
# Stop services
docker-compose stop

# Restore data
tar -xzf backup-YYYYMMDD.tar.gz

# Start services
docker-compose start
```

## 🔄 Updates

```bash
# Pull latest changes
git pull origin main

# Rebuild images
docker-compose build

# Restart with new images
docker-compose up -d

# Check status
docker-compose ps
```

## 🧪 Development

### Setup Dev Environment
```bash
./scripts/dev-setup.sh
```

### Run Tests
```bash
source venv/bin/activate
pytest
```

### Linting
```bash
black .
isort .
flake8 .
```

### Development Mode
```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

## 📋 Useful PromQL Queries

```promql
# Average temperature
avg(device_temperature)

# Max temperature by device
max(device_temperature) by (device_id)

# Rate of change
rate(device_counter[5m])

# Threshold alert
device_temperature > 80

# Multiple metrics
device_temperature or device_humidity
```

## 📝 Useful LogQL Queries

```logql
# All logs for a job
{job="sentio"}

# Error logs
{job="sentio"} |= "error"

# Exclude info logs
{job="sentio"} != "info"

# JSON field filter
{job="sentio"} | json | level="error"

# Count by level
sum(count_over_time({job="sentio"}[1h])) by (level)
```

## 🔧 Common Tasks

### Change Admin Password
1. Login to dashboard
2. Go to Settings → Users
3. Click admin → Change Password

Or via database:
```bash
docker-compose exec postgres psql -U sentio -d sentio
UPDATE users SET password_hash = '$2b$12$...' WHERE username = 'admin';
```

### Add New Device
1. Edit `config/connectors.yml`
2. Add device configuration
3. Restart connectors:
   ```bash
   docker-compose restart connectors
   ```

### Clear Old Data
```bash
# VictoriaMetrics
docker-compose stop victoriametrics
rm -rf data/victoriametrics/*
docker-compose start victoriametrics

# Loki
docker-compose exec loki rm -rf /loki/chunks/*
docker-compose restart loki
```

### Enable TLS
1. Get certificates
2. Configure nginx reverse proxy
3. Update environment variables
4. See [examples.md](examples.md#tlsssl-setup)

## 🆘 Getting Help

- 📖 [Full Documentation](docs/README.md)
- ❓ [FAQ](docs/FAQ.md)
- 🔧 [Troubleshooting Guide](docs/troubleshooting.md)
- 💬 [GitHub Discussions](https://github.com/NickScherbakov/sentio-iot/discussions)
- 🐛 [Report Bug](https://github.com/NickScherbakov/sentio-iot/issues)

## 🔗 Quick Links

- [GitHub Repository](https://github.com/NickScherbakov/sentio-iot)
- [Documentation](docs/README.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Roadmap](ROADMAP.md)
- [Changelog](CHANGELOG.md)

---

**Pro Tip:** Bookmark this page for quick reference! 📌

Last updated: November 2024
