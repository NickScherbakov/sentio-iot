# Configuration Guide

## Environment Variables

### API Server
```bash
# Database
DATABASE_URL=postgresql://sentio:sentio@postgres:5432/sentio

# Storage backends
VICTORIAMETRICS_URL=http://victoriametrics:8428
LOKI_URL=http://loki:3100
TEMPO_URL=http://tempo:3200

# Cache and queue
REDIS_URL=redis://redis:6379

# Security
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# CORS
CORS_ORIGINS=["http://localhost:3000"]
```

## Connector Configuration

### Home Assistant

```yaml
homeassistant:
  enabled: true
  url: "http://homeassistant:8123"
  token: "your-long-lived-access-token"
  poll_interval: 30  # seconds
```

To get a Home Assistant token:
1. Go to Profile > Long-Lived Access Tokens
2. Create a new token
3. Copy and paste into config

### Zigbee (via Zigbee2MQTT)

```yaml
zigbee:
  enabled: true
  mqtt_broker: "localhost"
  mqtt_port: 1883
  mqtt_topic: "zigbee2mqtt/#"
  mqtt_username: ""  # optional
  mqtt_password: ""  # optional
  poll_interval: 10
```

### Modbus

```yaml
modbus:
  - enabled: true
    name: "PLC-1"
    host: "192.168.1.100"
    port: 502
    unit_id: 1
    poll_interval: 60
    timeout: 10
    registers:
      - name: "temperature"
        address: 0
        count: 1
        type: "holding"  # or "input", "coil"
        scale: 0.1       # optional multiplier
        offset: 0        # optional offset
      - name: "pressure"
        address: 1
        count: 1
        type: "holding"
```

### OPC-UA

```yaml
opcua:
  - enabled: true
    name: "SCADA-1"
    endpoint: "opc.tcp://192.168.1.200:4840"
    security_policy: "None"  # or "Basic256Sha256"
    security_mode: "None"    # or "Sign", "SignAndEncrypt"
    username: ""  # optional
    password: ""  # optional
    poll_interval: 30
    nodes:
      - id: "ns=2;i=2"
        name: "temperature_sensor"
      - id: "ns=2;i=3"
        name: "pressure_sensor"
```

## Storage Configuration

### VictoriaMetrics

Edit retention period:
```bash
# In docker-compose.yml
command:
  - "--retentionPeriod=12"  # months
```

### Loki

Edit `config/loki-config.yml`:
```yaml
limits_config:
  retention_period: 744h  # 31 days
  ingestion_rate_mb: 10
  ingestion_burst_size_mb: 20
```

### Tempo

Edit `config/tempo-config.yml`:
```yaml
compactor:
  compaction:
    block_retention: 1h
```

## AI Engine Configuration

Configure in `ai-engine/main.py`:

```python
# Anomaly detection
self.contamination = 0.1  # Expected proportion of outliers (10%)

# Alert thresholds
self.alert_threshold = 0.8  # Minimum score to trigger alert

# Cooldown periods
self.cooldown_period = 300  # 5 minutes between same alerts
```

## Security Configuration

### JWT Secret Key

Generate a secure key:
```bash
openssl rand -hex 32
```

Add to `.env`:
```bash
JWT_SECRET_KEY=your-generated-key
```

### TLS/HTTPS

Add TLS certificates to `certs/` directory and configure in `docker-compose.yml`:

```yaml
api:
  volumes:
    - ./certs:/app/certs
  environment:
    - TLS_CERT=/app/certs/cert.pem
    - TLS_KEY=/app/certs/key.pem
```

## Dashboard Configuration

Create `dashboard/.env.local`:
```bash
VITE_API_URL=http://localhost:8080/api/v1
VITE_WS_URL=ws://localhost:8080/ws
```

## Scaling Configuration

### Multiple Collector Instances

```yaml
collectors:
  deploy:
    replicas: 3
  environment:
    - INSTANCE_ID=${HOSTNAME}
```

### Load Balancing

Use nginx or traefik for load balancing:
```nginx
upstream api_backend {
    server api1:8080;
    server api2:8080;
    server api3:8080;
}
```

## Advanced Configuration

### Custom Metrics

Add custom metric definitions in collectors:
```python
custom_metric = Gauge('custom_metric_name', 'Description')
custom_metric.set(value)
```

### Custom Log Parsers

Extend the log collector with custom parsers:
```python
def custom_parser(log_line):
    # Parse custom log format
    return parsed_data
```

### Retention Policies

Configure different retention for different data types:
- Metrics: 12 months (adjustable)
- Logs: 31 days (adjustable)
- Traces: 7 days (adjustable)

## Best Practices

1. **Use environment-specific configs**: Separate dev, staging, production configs
2. **Secure secrets**: Use secret management tools (Vault, AWS Secrets Manager)
3. **Monitor resource usage**: Set appropriate limits based on your workload
4. **Regular backups**: Backup PostgreSQL database and configurations
5. **Log rotation**: Configure log rotation for all services
