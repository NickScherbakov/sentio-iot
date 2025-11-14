# Sentio IoT - Distributed Observability Platform

**Sentio IoT** is an open-source, distributed observability platform designed specifically for IoT and edge devices. It provides scalable collection, analysis, and visualization of metrics, logs, and traces with AI-powered alerting, predictive fault detection, and ready-made connectors for popular IoT protocols.

## 📚 Documentation Index

### Getting Started
- **[Installation Guide](installation.md)** - Step-by-step installation instructions
- **[Quick Start](../README.md#-quick-start)** - Get running in 5 minutes
- **[Configuration Guide](configuration.md)** - Configure connectors and services
- **[Example Configurations](examples.md)** - Ready-to-use configuration examples

### Understanding Sentio IoT
- **[Architecture Overview](architecture.md)** - Technical architecture and design
- **[Comparison Guide](comparison.md)** - Compare with alternatives (Grafana, Prometheus, etc.)
- **[API Reference](api.md)** - REST API and WebSocket documentation

### Deployment
- **[Deployment Guide](deployment.md)** - Production deployment scenarios
- **[Docker Compose](../docker-compose.yml)** - Container orchestration
- **[Security Best Practices](../SECURITY.md)** - Secure your deployment

### Contributing
- **[Contributing Guide](../CONTRIBUTING.md)** - How to contribute
- **[Roadmap](../ROADMAP.md)** - Future features and plans
- **[Code of Conduct](../CODE_OF_CONDUCT.md)** - Community guidelines

## 🚀 Features

### Core Capabilities
- **Multi-Signal Observability**: Unified collection of metrics, logs, and distributed traces
- **Scalable Architecture**: Horizontally scalable components for high-throughput environments
- **Real-Time Dashboard**: Modern, responsive web interface with live data updates
- **Cloud & On-Premises**: Deploy anywhere - cloud, on-premises, or hybrid

### AI-Powered Intelligence
- **Anomaly Detection**: Machine learning-based anomaly detection using Isolation Forest
- **Predictive Maintenance**: Early fault prediction to prevent device failures
- **Intelligent Alerting**: Context-aware alerts with automatic cooldown and deduplication
- **Continuous Learning**: Models retrain periodically on historical data

### Protocol Connectors
- **Home Assistant**: Native integration with Home Assistant for smart home monitoring
- **Zigbee**: MQTT-based Zigbee device integration (via Zigbee2MQTT)
- **Modbus**: Industrial protocol support for Modbus TCP devices
- **OPC-UA**: Industrial Ethernet integration for OPC-UA servers

### Data Storage
- **VictoriaMetrics**: High-performance time-series database for metrics
- **Loki**: Efficient log aggregation and storage
- **Tempo**: Distributed tracing backend
- **PostgreSQL**: Metadata and configuration storage
- **Redis**: Caching and message queue

## 📋 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Dashboard (React)                     │
│          Metrics Explorer │ Logs │ Traces │ Devices          │
└───────────────────────────┬─────────────────────────────────┘
                            │
                    ┌───────▼────────┐
                    │   API Server   │
                    │   (FastAPI)    │
                    └───┬───────┬────┘
                        │       │
        ┌───────────────┤       ├──────────────┐
        │               │       │              │
   ┌────▼────┐    ┌────▼────┐  │    ┌────────▼────────┐
   │  VictoriaMetrics  │    │  Loki   │  │    │  Tempo (Traces) │
   │   (Metrics)   │    │  (Logs) │  │    │                 │
   └────▲────┘    └────▲────┘  │    └────────▲────────┘
        │               │       │              │
        │         ┌─────▼───────▼────┐        │
        │         │   Collectors      │        │
        │         │   Service         │        │
        │         └─────▲─────────────┘        │
        │               │                      │
        │         ┌─────▼─────────┐           │
        │         │  Connectors   │           │
        │         │   Service     │           │
        │         └───┬───┬───┬───┘           │
        │             │   │   │               │
        │    ┌────────┘   │   └────────┐     │
        │    │            │            │     │
   ┌────▼────▼─┐   ┌─────▼──────┐  ┌─▼─────▼───┐
   │Home Assistant│   │  Zigbee   │  │  Modbus   │
   │             │   │  Devices  │  │  OPC-UA   │
   └─────────────┘   └───────────┘  └───────────┘
                            │
                    ┌───────▼────────┐
                    │   AI Engine    │
                    │   (ML Models)  │
                    └────────────────┘
```

## 🛠️ Quick Start

### Prerequisites
- Docker & Docker Compose
- 4GB+ RAM
- 10GB+ disk space

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/NickScherbakov/sentio-iot.git
cd sentio-iot
```

2. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Start the platform**
```bash
docker-compose up -d
```

4. **Access the dashboard**
- Open http://localhost:3000
- Login with default credentials: `admin` / `admin`

### Deployment Options

#### Cloud Deployment
Deploy to any cloud provider (AWS, GCP, Azure, DigitalOcean):
```bash
# Using docker-compose
docker-compose -f docker-compose.yml -f docker-compose.cloud.yml up -d
```

#### On-Premises Deployment
For air-gapped or on-premises environments:
```bash
# Build images locally
docker-compose build

# Deploy
docker-compose up -d
```

## 📝 Configuration

### Connector Configuration

Edit `config/connectors.yml` to configure your device integrations:

```yaml
# Home Assistant
homeassistant:
  enabled: true
  url: "http://homeassistant:8123"
  token: "your-long-lived-access-token"
  poll_interval: 30

# Zigbee via MQTT
zigbee:
  enabled: true
  mqtt_broker: "localhost"
  mqtt_port: 1883
  mqtt_topic: "zigbee2mqtt/#"

# Modbus devices
modbus:
  - host: "192.168.1.100"
    port: 502
    registers:
      - name: "temperature"
        address: 0

# OPC-UA servers
opcua:
  - endpoint: "opc.tcp://192.168.1.200:4840"
    nodes:
      - id: "ns=2;i=2"
        name: "temperature_sensor"
```

### API Configuration

Configure the API server in `api/config.py` or via environment variables:

```bash
# Database
DATABASE_URL=postgresql://sentio:sentio@postgres:5432/sentio

# Storage backends
VICTORIAMETRICS_URL=http://victoriametrics:8428
LOKI_URL=http://loki:3100
TEMPO_URL=http://tempo:3200

# Security
JWT_SECRET_KEY=your-secret-key-here
```

## 🔌 API Endpoints

### Authentication
```
POST /api/v1/auth/login
```

### Metrics
```
POST /api/v1/metrics/query
GET  /api/v1/metrics/series
```

### Logs
```
POST /api/v1/logs/query
GET  /api/v1/logs/labels
```

### Traces
```
POST /api/v1/traces/query
GET  /api/v1/traces/{trace_id}
```

### Devices
```
GET    /api/v1/devices
POST   /api/v1/devices
GET    /api/v1/devices/{id}
PUT    /api/v1/devices/{id}
DELETE /api/v1/devices/{id}
```

### Alerts
```
GET    /api/v1/alerts
POST   /api/v1/alerts
GET    /api/v1/alerts/{id}
PUT    /api/v1/alerts/{id}
DELETE /api/v1/alerts/{id}
```

### AI Insights
```
GET /api/v1/ai/anomalies
GET /api/v1/ai/predictions
```

## 📊 Dashboard Features

### Main Dashboard
- Real-time system status
- Active device count
- Metrics throughput
- Recent anomalies and predictions
- Resource utilization charts

### Metrics Explorer
- PromQL query interface
- Time-series visualization
- Multiple metric comparison
- Export capabilities

### Logs Explorer
- LogQL query interface
- Full-text search
- Label filtering
- Live tail mode

### Traces Viewer
- Distributed trace visualization
- Service dependency graph
- Performance analysis
- Error tracking

### Device Management
- Device inventory
- Protocol configuration
- Status monitoring
- Metadata management

### Alert Management
- Alert rule creation
- Notification channels
- Alert history
- Severity configuration

## 🤖 AI Engine

### Anomaly Detection
The AI engine uses Isolation Forest algorithm to detect anomalies:
- Automatic model training on historical data
- Real-time anomaly scoring
- Configurable sensitivity
- Context-aware detection

### Predictive Maintenance
Predicts potential device failures:
- Statistical analysis of metrics
- Trend detection
- Risk level assessment
- Time-to-failure estimation

### Intelligent Alerting
Smart alert management:
- Cooldown periods to prevent alert storms
- Severity calculation
- Context enrichment
- Deduplication

## 🔒 Security

- **Authentication**: JWT-based authentication
- **Authorization**: Role-based access control (RBAC)
- **Transport Security**: TLS/mTLS support for device communication
- **Secret Management**: Environment-based configuration
- **API Security**: Rate limiting and request validation

## 🧪 Development

### Running Locally
```bash
# API Server
cd api
pip install -r requirements.txt
uvicorn main:app --reload

# Dashboard
cd dashboard
npm install
npm run dev

# Collectors
cd collectors
pip install -r requirements.txt
python main.py
```

### Testing
```bash
# Run tests
pytest

# With coverage
pytest --cov=api --cov-report=html
```

## 📈 Performance

- **Metrics Ingestion**: Up to 100k metrics/second per collector instance
- **Log Ingestion**: Up to 50k logs/second per collector instance
- **Query Latency**: < 100ms for most queries
- **Data Retention**: Configurable (default: 12 months)
- **Scalability**: Horizontal scaling for all components

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [VictoriaMetrics](https://victoriametrics.com/)
- Logs by [Grafana Loki](https://grafana.com/oss/loki/)
- Traces by [Grafana Tempo](https://grafana.com/oss/tempo/)
- UI with [Material-UI](https://mui.com/)

## 📞 Support

- Documentation: [docs/](docs/)
- Issues: [GitHub Issues](https://github.com/NickScherbakov/sentio-iot/issues)
- Discussions: [GitHub Discussions](https://github.com/NickScherbakov/sentio-iot/discussions)

## 🗺️ Roadmap

- [ ] Additional protocol connectors (MQTT, CoAP, BACnet)
- [ ] Advanced ML models (LSTM, Prophet)
- [ ] Mobile application
- [ ] Plugin system
- [ ] Multi-tenancy support
- [ ] Kubernetes operator
- [ ] Edge agent for resource-constrained devices
- [ ] Integration with popular notification services (Slack, PagerDuty, etc.)

---

**Sentio IoT** - Making IoT observability accessible to everyone.
