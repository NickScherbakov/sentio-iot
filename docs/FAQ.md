# Frequently Asked Questions (FAQ)

Common questions and answers about Sentio IoT.

## General Questions

### What is Sentio IoT?

Sentio IoT is an open-source distributed observability platform designed specifically for IoT and edge devices. It provides unified monitoring of metrics, logs, and traces with AI-powered analytics.

### Who should use Sentio IoT?

Sentio IoT is ideal for:
- IoT developers and operators
- Industrial automation engineers
- Smart home enthusiasts
- DevOps teams managing edge devices
- Anyone monitoring distributed IoT deployments

### Is Sentio IoT free?

Yes! Sentio IoT is completely free and open-source under the MIT License. You can use it commercially, modify it, and distribute it freely.

### What's the difference between Sentio IoT and Grafana?

Grafana is a visualization platform that requires separate data sources. Sentio IoT is a complete observability stack with built-in storage, AI analytics, and IoT-specific connectors. See our [Comparison Guide](comparison.md) for details.

## Installation & Setup

### What are the system requirements?

**Minimum:**
- 2 CPU cores
- 4 GB RAM
- 20 GB storage
- Docker 20.10+
- Docker Compose 2.0+

**Recommended (Production):**
- 4+ CPU cores
- 8+ GB RAM
- 100+ GB SSD storage
- Linux OS (Ubuntu 22.04 LTS recommended)

### How long does installation take?

With Docker Compose: **5-10 minutes** for first-time setup, including image downloads.

### Can I run Sentio IoT on Raspberry Pi?

Yes! Sentio IoT supports ARM64 architecture. We recommend:
- Raspberry Pi 4 (4GB+ RAM)
- Raspberry Pi 5
- 32GB+ SD card
- Active cooling

### Do I need Kubernetes?

No. Sentio IoT runs perfectly with Docker Compose. Kubernetes support is planned for v1.5 but is not required.

## Configuration

### How do I change the default password?

1. Edit `.env` file
2. Change `DEFAULT_ADMIN_PASSWORD`
3. Restart services: `docker-compose restart api`
4. Login and change password in dashboard

**Important:** Change default credentials before production deployment!

### Can I use existing databases?

Yes! You can configure Sentio IoT to use existing:
- PostgreSQL database
- Redis instance

Just update the connection strings in `.env` file.

### How do I add a new device?

1. Configure the appropriate connector in `config/connectors.yml`
2. Restart connectors: `docker-compose restart connectors`
3. Device will appear in dashboard automatically

See [Example Configurations](examples.md) for connector setup.

### Can I collect metrics from custom applications?

Yes! Multiple options:
- **Prometheus format**: Expose metrics at `/metrics` endpoint
- **StatsD**: Send metrics to collectors
- **REST API**: Push metrics via API
- **Custom connector**: Write your own connector

## Performance & Scaling

### How many devices can Sentio IoT handle?

With default configuration:
- **Metrics**: 100,000+ metrics/second
- **Logs**: 50,000+ logs/second
- **Devices**: Thousands of devices

Scale horizontally by adding more collector/connector replicas.

### How do I scale Sentio IoT?

1. **Vertical scaling**: Increase resources for containers
2. **Horizontal scaling**: Add more replicas:
   ```bash
   docker-compose up --scale collectors=3 --scale connectors=3
   ```
3. **Kubernetes**: Deploy with Kubernetes (v1.5+)

### How much storage do I need?

Depends on metrics volume and retention. Rough estimates:

- **1000 devices** reporting every 30s: ~50 GB/month
- **10,000 devices** reporting every 30s: ~500 GB/month

VictoriaMetrics provides excellent compression (10x better than Prometheus).

### Can I reduce storage requirements?

Yes:
1. Adjust retention periods in `config/`
2. Enable downsampling for old data
3. Configure selective metric collection
4. Use data compression

## Features & Functionality

### Does Sentio IoT support alerting?

Yes! Features include:
- Rule-based alerts
- AI-powered anomaly alerts
- Email notifications
- Webhook integrations
- Alert cooldown periods

### Can I create custom dashboards?

Currently, dashboards are pre-built. Custom dashboard builder is planned for v1.1. You can:
- Modify React dashboard code
- Use Grafana alongside Sentio IoT
- Query data via API for external tools

### Does it support multi-tenancy?

Multi-tenancy support is planned for v1.2. Current version uses single-tenant model with RBAC.

### Can I export data?

Yes! Multiple export options:
- PromQL API for metrics
- LogQL API for logs
- REST API for raw data
- CSV/JSON export (via API)
- Prometheus remote read

### Does it work offline?

Yes! Sentio IoT can run completely offline (air-gapped). All components run locally without internet requirements.

## Protocols & Integrations

### Which protocols are supported?

**Current:**
- Home Assistant (REST API)
- Zigbee (via MQTT)
- Modbus TCP
- OPC-UA

**Planned (v1.4):**
- MQTT direct
- CoAP
- BACnet
- Z-Wave

### How do I connect to Home Assistant?

1. Get long-lived access token from Home Assistant
2. Configure in `config/connectors.yml`:
   ```yaml
   home_assistant:
     enabled: true
     base_url: "http://homeassistant.local:8123"
     token: "your-token-here"
   ```
3. Restart connectors

See [Example Configurations](examples.md#home-assistant-integration) for details.

### Can I use MQTT?

Yes! Zigbee connector supports MQTT. Direct MQTT support planned for v1.4.

### Does it integrate with Grafana?

Yes! You can:
- Use VictoriaMetrics as Prometheus data source
- Use Loki as log data source
- Use Tempo as trace data source

All are Grafana-compatible.

## Security

### Is Sentio IoT secure?

Sentio IoT follows security best practices:
- JWT authentication
- Password hashing (bcrypt)
- TLS/SSL support
- RBAC authorization
- Regular security updates
- Vulnerability scanning

See [Security Policy](../SECURITY.md) for details.

### How do I enable HTTPS?

1. Obtain SSL certificates
2. Configure reverse proxy (nginx)
3. Update `REACT_APP_API_URL` to use `https://`

Example nginx config in [Example Configurations](examples.md#tlsssl-setup).

### Can I use SSO/SAML?

SAML/OAuth support is planned for v1.2. Currently supports JWT authentication only.

### How do I secure Modbus/OPC-UA connections?

- **Modbus**: Use VPN or private network
- **OPC-UA**: Supports security policies (Basic256Sha256)
- **General**: Run on isolated network, use firewall rules

## Troubleshooting

### Services won't start

```bash
# Check logs
docker-compose logs

# Common issues:
# 1. Port conflicts - Change ports in docker-compose.yml
# 2. Insufficient memory - Increase Docker memory limit
# 3. Missing directories - Run: mkdir -p data/{victoriametrics,loki,tempo}
```

### Dashboard shows no data

1. Check if connectors are running: `docker-compose ps`
2. Verify connector configuration in `config/connectors.yml`
3. Check connector logs: `docker-compose logs connectors`
4. Verify devices are reachable

### API returns 401 Unauthorized

1. Check if token is valid
2. Verify token is included in request headers
3. Check token expiration (`JWT_EXPIRE_MINUTES` in `.env`)
4. Login again to get new token

### High memory usage

1. Check retention periods - reduce if too long
2. Limit metric labels - too many unique series
3. Increase memory allocation for containers
4. Enable downsampling for old data

### Database connection errors

1. Check if PostgreSQL is running: `docker-compose ps postgres`
2. Verify `DATABASE_URL` in `.env`
3. Check database logs: `docker-compose logs postgres`
4. Verify credentials

See [Troubleshooting Guide](troubleshooting.md) for more issues.

## Development

### How can I contribute?

We welcome contributions! See [Contributing Guide](../CONTRIBUTING.md) for:
- Code contribution process
- Development setup
- Coding standards
- PR guidelines

### Where do I report bugs?

Open an issue on GitHub:
1. Use bug report template
2. Include logs and system info
3. Provide reproduction steps

[Report a Bug](https://github.com/NickScherbakov/sentio-iot/issues/new?template=bug_report.yml)

### Can I add support for new protocols?

Yes! Protocol connectors are modular:
1. Study existing connectors in `connectors/`
2. Follow connector interface
3. Submit PR with tests
4. Update documentation

### How do I run tests?

```bash
# Setup development environment
./scripts/dev-setup.sh

# Run all tests
pytest

# Run specific tests
pytest api/tests/

# With coverage
pytest --cov
```

## Deployment

### Can I deploy to AWS/GCP/Azure?

Yes! Sentio IoT can run on any cloud:
- AWS: ECS, EKS, EC2
- GCP: GKE, Compute Engine
- Azure: AKS, VMs
- DigitalOcean: Droplets, Kubernetes

See [Deployment Guide](deployment.md) for cloud-specific instructions.

### What about Kubernetes?

Kubernetes manifests and Helm charts are planned for v1.5. Currently use Docker Compose.

### How do I backup data?

```bash
# Backup script (run regularly)
./scripts/backup.sh

# Or manually:
tar -czf backup.tar.gz data/
```

Backup includes:
- Metrics data
- Logs
- Traces
- PostgreSQL database
- Configuration files

### Can I run in production?

Yes! Sentio IoT is production-ready. Recommendations:
- Use separate database server
- Enable TLS/SSL
- Regular backups
- Monitoring and alerting
- High availability setup

See [Deployment Guide](deployment.md) for production checklist.

## Comparison & Alternatives

### Should I use Sentio IoT or Prometheus?

Use **Sentio IoT** if you need:
- IoT protocol connectors
- Unified metrics + logs + traces
- AI analytics
- Easier setup

Use **Prometheus** if you need:
- Maximum ecosystem integrations
- Existing Prometheus setup
- Infrastructure monitoring only

See [Comparison Guide](comparison.md) for detailed comparison.

### Can I migrate from Grafana?

Yes! Migration path:
1. Keep existing Prometheus exporters
2. Point VictoriaMetrics to scrape them
3. Import Prometheus data
4. Gradually migrate dashboards

### Is there commercial support?

Community support via GitHub. Commercial support options are being developed. Contact via GitHub Discussions if interested.

## Licensing

### Can I use Sentio IoT commercially?

Yes! MIT License allows:
- Commercial use
- Modification
- Distribution
- Private use

### Do I need to open-source my modifications?

No. MIT License does not require sharing modifications.

### Can I sell Sentio IoT-based products?

Yes! You can build and sell products/services using Sentio IoT.

### What attribution is required?

MIT License requires:
- Include original license text
- Include copyright notice

That's it! Very permissive.

## Getting Help

### Where can I get help?

Multiple channels:
- 📖 [Documentation](README.md)
- 💬 [GitHub Discussions](https://github.com/NickScherbakov/sentio-iot/discussions)
- 🐛 [Issue Tracker](https://github.com/NickScherbakov/sentio-iot/issues)
- 📧 Email: Open an issue first

### How do I ask a good question?

Include:
1. What you're trying to do
2. What you've already tried
3. Error messages/logs
4. System information
5. Configuration (sanitized)

### Response time?

Community project - response times vary:
- Critical bugs: 24-48 hours
- Feature requests: Variable
- Questions: Variable

Contributions welcome to help others!

## Still Have Questions?

Can't find your answer? Try:

1. 📖 [Read the Full Documentation](README.md)
2. 🔍 [Search Existing Issues](https://github.com/NickScherbakov/sentio-iot/issues)
3. 💬 [Ask in Discussions](https://github.com/NickScherbakov/sentio-iot/discussions)
4. 🆕 [Open a New Issue](https://github.com/NickScherbakov/sentio-iot/issues/new?template=question.yml)

---

**Don't see your question?** [Suggest an addition to this FAQ](https://github.com/NickScherbakov/sentio-iot/issues/new)

Last updated: November 2024
