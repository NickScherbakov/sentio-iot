# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub Actions CI/CD workflows
- Automated testing and linting
- Docker image build and publish workflow
- CodeQL security scanning
- Dependabot for dependency updates
- Automated release workflow
- Pre-commit hooks configuration
- Development environment setup script
- Comprehensive testing infrastructure
- Enhanced OpenAPI/Swagger documentation
- Community contribution infrastructure:
  - Issue templates (bug, feature, question)
  - Pull request template
  - Code of Conduct
  - Security policy
  - Contributing guidelines enhancements
  - Funding configuration
- Documentation enhancements:
  - Comprehensive FAQ
  - Troubleshooting guide
  - Comparison with alternatives (Grafana, Prometheus, etc.)
  - Example configurations for all use cases
  - Versioning and release process documentation
  - Contributors recognition system
- Project maturity improvements:
  - ROADMAP with future plans
  - GitHub topics recommendations
  - Enhanced README with better visuals and structure
  - Architecture diagram (ASCII art)
  - Use cases section

### Changed
- Improved README structure and visual appeal
- Enhanced documentation index with cross-references
- Better API documentation with OpenAPI metadata
- Reorganized documentation for better navigation

### Infrastructure
- CI pipeline with Python and JavaScript linting
- Automated Docker image builds for multiple architectures
- Security scanning with Trivy and CodeQL
- Integration testing in CI
- Docker Compose development overrides

## [1.0.0] - 2024-11-13

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
  - VictoriaMetrics for time-series metrics (12-month retention)
  - Loki for log aggregation (31-day retention)
  - Tempo for distributed tracing (7-day retention)
  - PostgreSQL for metadata
  - Redis for caching and queuing
- AI-powered features:
  - Anomaly detection using Isolation Forest
  - Predictive maintenance with risk assessment
  - Intelligent alerting with cooldown periods
  - Automatic model training on historical data
- Dashboard features:
  - Real-time system overview with WebSocket updates
  - Metrics explorer with PromQL queries
  - Logs explorer with LogQL queries
  - Traces visualization
  - Device management interface
  - Alert management interface
- Security features:
  - JWT-based authentication
  - Role-based access control foundation
  - TLS/mTLS support structure
  - Password hashing with bcrypt
  - Environment-based secret management
- Documentation:
  - Comprehensive README with quick start
  - Installation guide
  - Configuration reference
  - API documentation
  - Architecture overview
  - Deployment guide (cloud and on-premises)
  - Contributing guidelines
- Deployment options:
  - Docker Compose for local and production
  - Cloud deployment guides (AWS, GCP, Azure, DigitalOcean)
  - On-premises deployment guide
  - High availability setup guidance
- DevOps:
  - Quick start script
  - Example environment configuration
  - Docker multi-stage builds for optimization
  - Comprehensive .gitignore

### Performance
- 100,000+ metrics per second ingestion capacity
- Sub-100ms query latency (typical)
- Efficient data compression with VictoriaMetrics
- Async/await throughout the stack
- Connection pooling and batching

### Security
- JWT secret key configuration
- Secure password handling with bcrypt
- Environment-based configuration
- Docker non-root users
- Network isolation via Docker networks
- No hardcoded credentials
- Secure defaults

## Future Versions

See [ROADMAP.md](ROADMAP.md) for planned features and timeline.

### v1.1 - Enhanced Monitoring (Q1 2025)
- Custom dashboard builder
- Advanced query capabilities
- Performance optimizations
- User experience improvements

### v1.2 - Enterprise Features (Q2 2025)
- Multi-tenancy support
- Advanced RBAC
- Compliance tools
- Team management

### v1.3 - Advanced AI (Q2 2025)
- Deep learning models
- Time series forecasting
- Root cause analysis
- Natural language queries

### v1.4 - Extended Protocol Support (Q3 2025)
- MQTT direct support
- CoAP protocol
- BACnet integration
- Z-Wave support
- Matter/Thread support

### v1.5 - Cloud & Edge (Q3 2025)
- Kubernetes manifests
- Helm charts
- Edge agent
- ARM architecture optimizations
- Cloud provider integrations

### v2.0 - Plugin System (Q4 2025)
- Plugin API and SDK
- Plugin marketplace
- Custom data sources
- Custom visualizations

## Release Notes Format

Each release includes:
- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security fixes

## Links

- [ROADMAP](ROADMAP.md) - Future plans
- [VERSIONING](VERSIONING.md) - Versioning policy
- [CONTRIBUTING](CONTRIBUTING.md) - How to contribute
- [SECURITY](SECURITY.md) - Security policy

---

For detailed commit history, see [GitHub Commits](https://github.com/NickScherbakov/sentio-iot/commits/main)
