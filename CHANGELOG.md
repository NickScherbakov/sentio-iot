# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-09

### Added
- Initial release of Sentio IoT distributed observability platform
- Core microservices architecture with 6 components:
  - FastAPI-based REST API server
  - Data collectors service for metrics, logs, and traces
  - Protocol connectors service
  - AI engine for anomaly detection and predictions
  - React-based web dashboard
  - Supporting infrastructure (databases, caches)
- Protocol connectors:
  - Home Assistant integration
  - Zigbee support via MQTT/Zigbee2MQTT
  - Modbus TCP connector for industrial devices
  - OPC-UA connector for industrial Ethernet
- Storage backends:
  - VictoriaMetrics for time-series metrics
  - Loki for log aggregation
  - Tempo for distributed tracing
  - PostgreSQL for metadata
  - Redis for caching and queuing
- AI-powered features:
  - Anomaly detection using Isolation Forest
  - Predictive maintenance with risk assessment
  - Intelligent alerting with cooldown periods
  - Automatic model training on historical data
- Dashboard features:
  - Real-time system overview
  - Metrics explorer with PromQL queries
  - Logs explorer with LogQL queries
  - Traces visualization
  - Device management interface
  - Alert management interface
- Security features:
  - JWT-based authentication
  - Role-based access control foundation
  - TLS/mTLS support structure
  - Environment-based secret management
- Documentation:
  - Comprehensive README
  - Installation guide
  - Configuration guide
  - Deployment guide (cloud and on-premises)
  - Contributing guidelines
  - API documentation
- Deployment options:
  - Docker Compose for local and production
  - Cloud deployment guides (AWS, GCP, Azure, DigitalOcean)
  - On-premises deployment guide
  - High availability setup guide
- DevOps:
  - Quick start script
  - Example environment configuration
  - Git ignore rules for build artifacts
  - Docker multi-stage builds for optimization

### Security
- JWT secret key configuration
- Secure password handling
- Environment-based configuration
- Docker non-root users
- Network isolation via Docker networks

## [Unreleased]

### Planned
- Kubernetes deployment manifests
- Helm charts for Kubernetes
- Additional protocol connectors (MQTT, CoAP, BACnet)
- Advanced ML models (LSTM, Prophet)
- Mobile application
- Plugin system for extensibility
- Multi-tenancy support
- Edge agent for resource-constrained devices
- Integration with notification services (Slack, PagerDuty)
- Grafana dashboards as alternative UI
- Performance optimizations
- Enhanced test coverage
- CI/CD pipeline configuration
- Automated backup and restore scripts
