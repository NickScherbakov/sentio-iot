# Example Configurations

This directory contains example configurations for various use cases with Sentio IoT.

## Home Assistant Integration

### Basic Setup

**File: `config/connectors.yml`**
```yaml
home_assistant:
  enabled: true
  base_url: "http://home-assistant.local:8123"
  token: "your-long-lived-access-token"
  poll_interval: 30
  entities:
    - sensor.temperature_living_room
    - sensor.humidity_bedroom
    - light.kitchen
    - switch.garden_lights
```

### Advanced Setup with Multiple Instances

```yaml
home_assistant:
  enabled: true
  instances:
    - name: "home"
      base_url: "http://192.168.1.10:8123"
      token: "home-token-here"
      poll_interval: 30
      
    - name: "office"
      base_url: "http://192.168.2.10:8123"
      token: "office-token-here"
      poll_interval: 60
      entities:
        - sensor.temperature_*
        - sensor.humidity_*
```

## Zigbee (MQTT) Integration

### Zigbee2MQTT Configuration

**File: `config/connectors.yml`**
```yaml
zigbee:
  enabled: true
  mqtt_broker: "mqtt://192.168.1.100:1883"
  mqtt_username: "zigbee"
  mqtt_password: "secure-password"
  base_topic: "zigbee2mqtt"
  devices:
    - friendly_name: "Living Room Motion Sensor"
      ieee_address: "0x00158d0001234567"
    - friendly_name: "Kitchen Temperature Sensor"
      ieee_address: "0x00158d0001234568"
```

## Modbus TCP Integration

### Industrial PLC Monitoring

**File: `config/connectors.yml`**
```yaml
modbus:
  enabled: true
  devices:
    - name: "plc_1"
      host: "192.168.10.10"
      port: 502
      slave_id: 1
      poll_interval: 5
      registers:
        - name: "temperature"
          type: "input"
          address: 1000
          count: 1
          data_type: "float32"
          unit: "°C"
          
        - name: "pressure"
          type: "input"
          address: 1002
          count: 1
          data_type: "float32"
          unit: "bar"
          
        - name: "motor_speed"
          type: "holding"
          address: 2000
          count: 1
          data_type: "uint16"
          unit: "rpm"
```

### Multiple Modbus Devices

```yaml
modbus:
  enabled: true
  devices:
    - name: "hvac_controller"
      host: "192.168.10.20"
      port: 502
      slave_id: 1
      poll_interval: 10
      registers:
        - name: "hvac_temperature"
          type: "input"
          address: 0
          count: 1
          data_type: "float32"
          
    - name: "power_meter"
      host: "192.168.10.21"
      port: 502
      slave_id: 1
      poll_interval: 5
      registers:
        - name: "power_consumption"
          type: "input"
          address: 0
          count: 2
          data_type: "float32"
          unit: "kW"
```

## OPC-UA Integration

### Factory Equipment Monitoring

**File: `config/connectors.yml`**
```yaml
opcua:
  enabled: true
  servers:
    - name: "factory_line_1"
      endpoint_url: "opc.tcp://192.168.20.10:4840"
      security_policy: "Basic256Sha256"
      security_mode: "SignAndEncrypt"
      username: "opcua_user"
      password: "secure-password"
      certificate_path: "/app/certs/client-cert.pem"
      private_key_path: "/app/certs/client-key.pem"
      poll_interval: 5
      nodes:
        - node_id: "ns=2;s=Temperature"
          display_name: "line1_temperature"
        - node_id: "ns=2;s=Pressure"
          display_name: "line1_pressure"
        - node_id: "ns=2;s=ProductionCount"
          display_name: "line1_production"
```

## AI Engine Configuration

### Anomaly Detection

**File: `config/ai-config.yml`**
```yaml
anomaly_detection:
  enabled: true
  model: "isolation_forest"
  parameters:
    contamination: 0.1
    n_estimators: 100
  training:
    interval_hours: 24
    min_samples: 1000
    lookback_days: 7
  metrics:
    - "device.temperature"
    - "device.pressure"
    - "device.vibration"
```

### Predictive Maintenance

```yaml
predictive_maintenance:
  enabled: true
  model: "statistical"
  parameters:
    window_size: 100
    threshold_multiplier: 2.5
  alerts:
    - metric: "bearing_temperature"
      warn_threshold: 70
      critical_threshold: 85
      cooldown_minutes: 30
    - metric: "motor_vibration"
      warn_threshold: 5.0
      critical_threshold: 10.0
```

## Alert Configuration

### Email Alerts

**File: `config/alerts.yml`**
```yaml
alerts:
  email:
    enabled: true
    smtp_server: "smtp.gmail.com"
    smtp_port: 587
    smtp_username: "alerts@example.com"
    smtp_password: "app-password"
    from_address: "sentio@example.com"
    to_addresses:
      - "admin@example.com"
      - "ops@example.com"
      
  rules:
    - name: "High Temperature Alert"
      metric: "device.temperature"
      condition: ">"
      threshold: 80
      duration_minutes: 5
      severity: "critical"
      notification_channels: ["email", "webhook"]
```

### Webhook Alerts

```yaml
alerts:
  webhook:
    enabled: true
    endpoints:
      - name: "slack"
        url: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
        method: "POST"
        headers:
          Content-Type: "application/json"
          
  rules:
    - name: "Device Offline Alert"
      metric: "device.heartbeat"
      condition: "missing"
      duration_minutes: 10
      severity: "warning"
      notification_channels: ["webhook"]
```

## Storage Configuration

### VictoriaMetrics

**File: `config/victoriametrics.yml`**
```yaml
victoriametrics:
  retention_period: "12months"
  max_concurrent_inserts: 32
  max_labels_per_timeseries: 30
  deduplication_interval: "1m"
  downsampling:
    enabled: true
    rules:
      - interval: "5m"
        retention: "1month"
      - interval: "1h"
        retention: "6months"
      - interval: "1d"
        retention: "2years"
```

### Loki

**File: `config/loki-config.yml`**
```yaml
auth_enabled: false

server:
  http_listen_port: 3100

ingester:
  lifecycler:
    address: 127.0.0.1
    ring:
      kvstore:
        store: inmemory
      replication_factor: 1
  chunk_idle_period: 5m
  chunk_retain_period: 30s
  max_chunk_age: 1h

schema_config:
  configs:
    - from: 2024-01-01
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

storage_config:
  boltdb_shipper:
    active_index_directory: /loki/index
    cache_location: /loki/cache
    shared_store: filesystem
  filesystem:
    directory: /loki/chunks

limits_config:
  retention_period: 744h  # 31 days
  enforce_metric_name: false
  reject_old_samples: true
  reject_old_samples_max_age: 168h

chunk_store_config:
  max_look_back_period: 0s

table_manager:
  retention_deletes_enabled: true
  retention_period: 744h
```

## Docker Compose Overrides

### Production Configuration

**File: `docker-compose.prod.yml`**
```yaml
version: '3.8'

services:
  api:
    environment:
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - DATABASE_URL=postgresql://user:password@postgres:5432/sentio
      - LOG_LEVEL=warning
    restart: always
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G

  victoriametrics:
    volumes:
      - /mnt/storage/victoriametrics:/victoria-metrics-data
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G

  postgres:
    environment:
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - /mnt/storage/postgres:/var/lib/postgresql/data
```

### High Availability Setup

**File: `docker-compose.ha.yml`**
```yaml
version: '3.8'

services:
  api:
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
        
  collectors:
    deploy:
      replicas: 2
      
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/nginx/certs
    depends_on:
      - api
```

## Environment Variables

### Complete .env Example

**File: `.env`**
```bash
# Database
DATABASE_URL=postgresql://sentio:sentio@postgres:5432/sentio
POSTGRES_PASSWORD=change-in-production

# Security
JWT_SECRET_KEY=generate-secure-random-string-here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440

# Storage URLs
VICTORIAMETRICS_URL=http://victoriametrics:8428
LOKI_URL=http://loki:3100
TEMPO_URL=http://tempo:3200
REDIS_URL=redis://redis:6379

# CORS
CORS_ORIGINS=http://localhost:3000,https://your-domain.com

# API Settings
API_PREFIX=/api/v1
API_WORKERS=4
LOG_LEVEL=info

# Dashboard
REACT_APP_API_URL=http://localhost:8080
REACT_APP_WS_URL=ws://localhost:8080

# Email (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=alerts@example.com
SMTP_PASSWORD=app-password

# Monitoring
ENABLE_METRICS=true
ENABLE_TRACING=true
ENABLE_PROFILING=false

# AI Engine
AI_MODEL_PATH=/app/models
AI_TRAINING_INTERVAL=86400  # 24 hours in seconds

# Feature Flags
FEATURE_ANOMALY_DETECTION=true
FEATURE_PREDICTIVE_MAINTENANCE=true
FEATURE_AUTO_SCALING=false
```

## Security Configurations

### TLS/SSL Setup

**File: `nginx-ssl.conf`**
```nginx
server {
    listen 443 ssl http2;
    server_name sentio.example.com;

    ssl_certificate /etc/nginx/certs/fullchain.pem;
    ssl_certificate_key /etc/nginx/certs/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://dashboard:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://api:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws {
        proxy_pass http://api:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## Custom Metrics

### Prometheus Exposition Format

**Example: Custom Device Exporter**
```python
from prometheus_client import Gauge, start_http_server
import time

# Define metrics
temperature = Gauge('device_temperature_celsius', 'Device temperature in Celsius', ['device_id', 'location'])
humidity = Gauge('device_humidity_percent', 'Device humidity in percent', ['device_id', 'location'])

# Update metrics
temperature.labels(device_id='dev001', location='warehouse').set(22.5)
humidity.labels(device_id='dev001', location='warehouse').set(45.0)

# Start HTTP server on port 8000
start_http_server(8000)
```

Then configure Sentio collectors to scrape:
```yaml
scrape_configs:
  - job_name: 'custom_devices'
    static_configs:
      - targets: ['device-exporter:8000']
```

## Need Help?

- 📖 [Full Documentation](README.md)
- 💬 [GitHub Discussions](https://github.com/NickScherbakov/sentio-iot/discussions)
- 🐛 [Report Issues](https://github.com/NickScherbakov/sentio-iot/issues)
