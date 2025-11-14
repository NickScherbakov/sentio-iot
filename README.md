<div align="center">

# 🌐 Sentio IoT

### Distributed Observability Platform for IoT & Edge Devices

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/NickScherbakov/sentio-iot/workflows/CI/badge.svg)](https://github.com/NickScherbakov/sentio-iot/actions)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-18-%2361DAFB.svg?style=flat&logo=react)](https://reactjs.org/)
[![GitHub Stars](https://img.shields.io/github/stars/NickScherbakov/sentio-iot?style=social)](https://github.com/NickScherbakov/sentio-iot/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/NickScherbakov/sentio-iot?style=social)](https://github.com/NickScherbakov/sentio-iot/network/members)

**Sentio IoT** is an open-source, enterprise-grade observability platform designed specifically for IoT and edge devices. Monitor metrics, logs, and traces across thousands of devices in real-time with AI-driven alerting, predictive maintenance, and native integrations.

[🚀 Quick Start](#-quick-start) •
[📖 Documentation](docs/README.md) •
[🗺️ Roadmap](ROADMAP.md) •
[🤝 Contributing](CONTRIBUTING.md) •
[💬 Discussions](https://github.com/NickScherbakov/sentio-iot/discussions)

</div>

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 🎯 Core Capabilities
- 📊 **Unified Observability** - Metrics, logs, and traces in one platform
- 🤖 **AI-Powered Analytics** - Anomaly detection & predictive maintenance
- 📈 **Horizontally Scalable** - Handle thousands of devices effortlessly
- 🎨 **Modern Dashboard** - Real-time visualizations with WebSocket updates

</td>
<td width="50%">

### 🔌 Connectivity & Security
- 🌐 **Multi-Protocol Support** - Home Assistant, Zigbee, Modbus, OPC-UA
- 🔒 **Enterprise Security** - JWT auth, RBAC, TLS/mTLS
- ☁️ **Flexible Deployment** - Cloud, on-premises, or hybrid
- 🐳 **Container-Native** - Full Docker & Kubernetes support

</td>
</tr>
</table>

## 🚀 Quick Start

Get up and running in under 5 minutes!

```bash
# Clone the repository
git clone https://github.com/NickScherbakov/sentio-iot.git
cd sentio-iot

# Start all services with Docker Compose
docker-compose up -d

# Wait for services to initialize (~30 seconds)
docker-compose ps

# Access the dashboard
open http://localhost:3000
# Default credentials: admin / admin (⚠️ Change in production!)
```

### 📦 What's Included

After running `docker-compose up`, you'll have:

| Service | Port | Description |
|---------|------|-------------|
| 🎨 Dashboard | 3000 | Web UI for monitoring and management |
| 🔌 API Server | 8080 | REST API and WebSocket endpoint |
| 📊 VictoriaMetrics | 8428 | Time-series metrics database |
| 📝 Loki | 3100 | Log aggregation system |
| 🔍 Tempo | 3200 | Distributed tracing backend |
| 💾 PostgreSQL | 5432 | Metadata and configuration store |
| 🚀 Redis | 6379 | Cache and message queue |

### 🎬 Next Steps

1. 📖 Read the [Full Documentation](docs/README.md)
2. ⚙️ Configure your [first device connector](docs/configuration.md)
3. 🎯 Set up [alerts and monitoring](docs/api.md)
4. 🚀 Plan your [production deployment](docs/deployment.md)

## 📖 Documentation

Comprehensive documentation to help you get started:

| Guide | Description |
|-------|-------------|
| 📘 [Getting Started](docs/README.md) | Complete overview and introduction |
| 🔧 [Installation](docs/installation.md) | Detailed installation instructions |
| ⚙️ [Configuration](docs/configuration.md) | Configuration reference and examples |
| 📋 [Examples](docs/examples.md) | Ready-to-use configuration examples |
| 🚀 [Deployment](docs/deployment.md) | Production deployment guide |
| 📚 [API Reference](docs/api.md) | REST API and WebSocket documentation |
| 🏗️ [Architecture](docs/architecture.md) | Technical architecture deep dive |
| ❓ [FAQ](docs/FAQ.md) | Frequently asked questions |
| 🔧 [Troubleshooting](docs/troubleshooting.md) | Common issues and solutions |
| 🆚 [Comparison](docs/comparison.md) | Compare with alternatives |

## 🛠️ Technology Stack

### Backend
- **FastAPI** (Python 3.11) - High-performance async API framework
- **aiohttp** - Async HTTP client/server
- **scikit-learn** - Machine learning library
- **OpenTelemetry** - Observability instrumentation

### Frontend
- **React 18** - Modern UI framework
- **Material-UI** - Professional component library
- **Recharts** - Powerful data visualization
- **Vite** - Lightning-fast build tool

### Storage & Infrastructure
- **VictoriaMetrics** - Fast, cost-effective time-series DB
- **Loki** - Horizontally-scalable log aggregation
- **Tempo** - High-scale distributed tracing backend
- **PostgreSQL 15** - Reliable relational database
- **Redis 7** - In-memory data structure store
- **Docker** - Containerization platform

## 🏗️ Architecture

Sentio IoT uses a modern microservices architecture designed for scalability and reliability:

```
┌─────────────────────────────────────────────────────────────────┐
│                         Dashboard (React)                        │
│                    http://localhost:3000                         │
└────────────────────────────┬────────────────────────────────────┘
                             │ REST/WebSocket
┌────────────────────────────┴────────────────────────────────────┐
│                      API Server (FastAPI)                        │
│              Authentication • Authorization • WebSocket           │
└─────┬──────────┬──────────┬──────────┬─────────────────────────┘
      │          │          │          │
      ▼          ▼          ▼          ▼
┌──────────┐ ┌──────┐ ┌──────┐ ┌──────────────┐
│Victoria  │ │ Loki │ │Tempo │ │  PostgreSQL  │
│ Metrics  │ │      │ │      │ │   & Redis    │
│(Metrics) │ │(Logs)│ │(Trace)│ │  (Metadata)  │
└──────────┘ └──────┘ └──────┘ └──────────────┘
      ▲          ▲        ▲
      │          │        │
┌─────┴──────────┴────────┴──────────────────────────────────────┐
│                    Collectors Service                            │
│               Metrics • Logs • Traces Ingestion                  │
└─────────────────────────────┬────────────────────────────────────┘
                              │
┌─────────────────────────────┴────────────────────────────────────┐
│                     Protocol Connectors                           │
│        Home Assistant • Zigbee • Modbus • OPC-UA                 │
└───────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴──────────┐
                    ▼                    ▼
              [IoT Devices]        [Industrial PLCs]
```

### Core Components

- **🎨 Dashboard**: Modern React SPA with Material-UI
- **🔌 API Server**: FastAPI with async/await for high concurrency
- **📊 Collectors**: High-throughput data ingestion service
- **🔗 Connectors**: Protocol-specific device integration layer
- **🤖 AI Engine**: Machine learning for anomaly detection
- **💾 Storage**: Best-in-class open-source data stores

## 🔌 Supported Protocols & Integrations

<table>
<tr>
<td width="50%">

### 🏠 Smart Home
- **Home Assistant** - Full API integration
- **Zigbee** - Via MQTT/Zigbee2MQTT
- **Z-Wave** - Coming in v1.4
- **Matter/Thread** - Roadmap

</td>
<td width="50%">

### 🏭 Industrial
- **Modbus TCP** - PLCs and sensors
- **OPC-UA** - Industrial Ethernet standard
- **BACnet** - Building automation (planned)
- **LonWorks** - Roadmap

</td>
</tr>
</table>

### 🔜 Coming Soon
MQTT, CoAP, KNX, and custom protocol support - see our [Roadmap](ROADMAP.md)

## 🤝 Contributing

We love contributions! Sentio IoT is built by the community, for the community.

### Ways to Contribute

- 🐛 **Report bugs** - Open an issue with details
- 💡 **Suggest features** - Share your ideas
- 📝 **Improve docs** - Help others get started
- 💻 **Submit PRs** - Fix bugs or add features
- ⭐ **Star the repo** - Show your support!

### Getting Started

1. Read our [Contributing Guide](CONTRIBUTING.md)
2. Check out [Good First Issues](https://github.com/NickScherbakov/sentio-iot/labels/good%20first%20issue)
3. Join discussions in [GitHub Discussions](https://github.com/NickScherbakov/sentio-iot/discussions)
4. Review our [Code of Conduct](CODE_OF_CONDUCT.md)

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/sentio-iot.git
cd sentio-iot

# Create a branch
git checkout -b feature/amazing-feature

# Make your changes and test
docker-compose up -d

# Commit and push
git commit -m "Add amazing feature"
git push origin feature/amazing-feature

# Open a Pull Request
```

## 🗺️ Roadmap

Check out our [Roadmap](ROADMAP.md) to see what's coming next! We're working on:

- 🎨 Custom dashboard builder
- 🏢 Multi-tenancy support
- 🧠 Advanced AI/ML models
- 📱 Mobile applications
- 🔌 Additional protocol support
- ☸️ Kubernetes deployment

Vote on features and suggest new ones in [GitHub Issues](https://github.com/NickScherbakov/sentio-iot/issues)!

## 📊 Project Stats

<div align="center">

![GitHub commit activity](https://img.shields.io/github/commit-activity/m/NickScherbakov/sentio-iot)
![GitHub issues](https://img.shields.io/github/issues/NickScherbakov/sentio-iot)
![GitHub pull requests](https://img.shields.io/github/issues-pr/NickScherbakov/sentio-iot)
![GitHub contributors](https://img.shields.io/github/contributors/NickScherbakov/sentio-iot)
![GitHub last commit](https://img.shields.io/github/last-commit/NickScherbakov/sentio-iot)

</div>

## 🙏 Acknowledgments

Sentio IoT builds on amazing open-source projects:

- [VictoriaMetrics](https://victoriametrics.com/) - Fast time-series database
- [Grafana Loki](https://grafana.com/oss/loki/) - Log aggregation system
- [Grafana Tempo](https://grafana.com/oss/tempo/) - Distributed tracing
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://reactjs.org/) - UI framework
- [Material-UI](https://mui.com/) - React components

Special thanks to all our [contributors](https://github.com/NickScherbakov/sentio-iot/graphs/contributors)!

## 🌟 Support the Project

If you find Sentio IoT useful, please consider:

- ⭐ **Star this repository** - It helps others discover the project
- 🐦 **Share on social media** - Spread the word
- 💬 **Join discussions** - Help build the community
- 🤝 **Contribute** - Code, docs, or ideas
- 💖 **Sponsor** - Support ongoing development

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### What this means:
- ✅ Commercial use allowed
- ✅ Modification allowed
- ✅ Distribution allowed
- ✅ Private use allowed
- ℹ️ License and copyright notice required

## 🔐 Security

Security is a top priority. Please review our [Security Policy](SECURITY.md) and report vulnerabilities responsibly.

## 📞 Contact & Community

- 💬 [GitHub Discussions](https://github.com/NickScherbakov/sentio-iot/discussions) - Ask questions, share ideas
- 🐛 [Issue Tracker](https://github.com/NickScherbakov/sentio-iot/issues) - Report bugs, request features
- 📧 Email - [Create an issue](https://github.com/NickScherbakov/sentio-iot/issues/new) for sensitive matters

## 🎯 Use Cases

Sentio IoT is perfect for:

- 🏠 **Smart Home Monitoring** - Track all your IoT devices in one place
- 🏭 **Industrial IoT** - Monitor factory equipment and sensors
- 🏢 **Building Management** - Oversee HVAC, lighting, and security systems
- 🌾 **Agriculture** - Monitor greenhouses and farm equipment
- 💡 **Energy Management** - Track power consumption and optimize usage
- 🚗 **Fleet Management** - Monitor vehicle telemetry and diagnostics

---

<div align="center">

**Built with ❤️ by the open-source community**

⭐ **Star us on GitHub!** — it motivates us to create more features ⭐

[Report Bug](https://github.com/NickScherbakov/sentio-iot/issues/new?template=bug_report.yml) •
[Request Feature](https://github.com/NickScherbakov/sentio-iot/issues/new?template=feature_request.yml) •
[Ask Question](https://github.com/NickScherbakov/sentio-iot/issues/new?template=question.yml)

</div>
