# Sentio IoT - Distributed Observability Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-%2320232a.svg?style=flat&logo=react&logoColor=%2361DAFB)](https://reactjs.org/)

**Sentio IoT** is an open-source, distributed observability platform designed specifically for IoT and edge devices. Monitor metrics, logs, and traces across thousands of devices in real-time with AI-driven alerting, predictive maintenance, and native integrations.

## ✨ Key Features

- 📊 **Unified Observability**: Metrics, logs, and distributed traces in one platform
- 🤖 **AI-Powered**: Anomaly detection, predictive maintenance, and intelligent alerting
- 🔌 **Protocol Support**: Home Assistant, Zigbee, Modbus, OPC-UA, and more
- 📈 **Scalable**: Horizontally scalable architecture for thousands of devices
- 🎨 **Modern UI**: Real-time dashboard with beautiful visualizations
- 🔒 **Secure**: JWT authentication, RBAC, and TLS/mTLS support
- ☁️ **Flexible Deployment**: Cloud, on-premises, or hybrid

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/NickScherbakov/sentio-iot.git
cd sentio-iot

# Start the platform
docker-compose up -d

# Access the dashboard
open http://localhost:3000
# Login: admin / admin
```

## 📖 Documentation

- [Full Documentation](docs/README.md)
- [Installation Guide](docs/installation.md)
- [Configuration Guide](docs/configuration.md)
- [API Reference](docs/api.md)
- [Deployment Guide](docs/deployment.md)

## 🏗️ Architecture

Sentio IoT consists of several microservices:

- **API Server**: RESTful API and WebSocket server
- **Collectors**: Metrics, logs, and traces collection
- **Connectors**: Protocol-specific device integrations
- **AI Engine**: Anomaly detection and predictive maintenance
- **Dashboard**: Modern web interface
- **Storage**: VictoriaMetrics, Loki, Tempo, PostgreSQL, Redis

## 🔌 Supported Protocols

- **Home Assistant**: Native integration for smart home devices
- **Zigbee**: Via MQTT/Zigbee2MQTT
- **Modbus**: Industrial protocol for PLCs and sensors
- **OPC-UA**: Industrial Ethernet standard
- **More coming**: MQTT, CoAP, BACnet, and custom protocols

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) to get started.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Support

If you find Sentio IoT useful, please consider giving it a ⭐️ on GitHub!

---

Built with ❤️ by the open-source community
