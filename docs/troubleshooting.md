# Troubleshooting Guide

This guide helps you diagnose and fix common issues with Sentio IoT.

## Quick Diagnostics

### Health Check

```bash
# Check if all services are running
docker-compose ps

# Check service health
curl http://localhost:8080/health
curl http://localhost:8428/health
curl http://localhost:3100/ready

# View all logs
docker-compose logs

# View specific service logs
docker-compose logs -f api
```

### Common Quick Fixes

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart api

# Rebuild and restart
docker-compose up -d --build

# Full reset (⚠️ deletes data)
docker-compose down -v
docker-compose up -d
```

## Installation Issues

### Port Already in Use

**Symptom:** Error: "port is already allocated"

**Cause:** Another application is using the port

**Solution:**
```bash
# Find process using port
sudo lsof -i :8080  # or whichever port

# Kill process (if safe)
sudo kill -9 <PID>

# Or change port in docker-compose.yml
ports:
  - "8081:8080"  # Change 8080 to 8081
```

### Docker Not Found

**Symptom:** "docker: command not found"

**Solution:**
```bash
# Install Docker
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# macOS
brew install docker

# Verify installation
docker --version
docker-compose --version
```

### Permission Denied

**Symptom:** "permission denied while trying to connect to Docker daemon"

**Solution:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Apply changes (logout/login or):
newgrp docker

# Verify
docker ps
```

### Insufficient Memory

**Symptom:** Services crash or OOMKilled

**Solution:**
```bash
# Check Docker memory limit
docker info | grep Memory

# Increase Docker memory (Docker Desktop)
# Settings → Resources → Memory → Increase to 8GB+

# Or reduce services memory in docker-compose.yml
deploy:
  resources:
    limits:
      memory: 512M
```

## Service-Specific Issues

### API Server

#### API Won't Start

**Check logs:**
```bash
docker-compose logs api
```

**Common causes:**

1. **Database connection failed**
   ```bash
   # Check PostgreSQL
   docker-compose logs postgres
   
   # Verify DATABASE_URL in .env
   DATABASE_URL=postgresql://sentio:sentio@postgres:5432/sentio
   ```

2. **Redis connection failed**
   ```bash
   # Check Redis
   docker-compose logs redis
   
   # Verify REDIS_URL in .env
   REDIS_URL=redis://redis:6379
   ```

3. **Port conflict**
   ```bash
   # Change port in docker-compose.yml
   ports:
     - "8081:8080"
   ```

#### API Returns 500 Errors

**Check:**
```bash
# View detailed logs
docker-compose logs -f api

# Check database connection
docker-compose exec postgres psql -U sentio -d sentio -c "\l"

# Restart API
docker-compose restart api
```

### Dashboard

#### Dashboard Shows White Screen

**Solutions:**

1. **Check API connection**
   ```bash
   curl http://localhost:8080/health
   ```

2. **Check environment variables**
   ```bash
   # In docker-compose.yml
   environment:
     - REACT_APP_API_URL=http://localhost:8080
   ```

3. **Clear browser cache**
   - Hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)

4. **Rebuild dashboard**
   ```bash
   docker-compose up -d --build dashboard
   ```

#### Dashboard Can't Connect to API

**Check CORS configuration:**

```python
# In api/config.py
CORS_ORIGINS = ["http://localhost:3000", "http://localhost:8080"]
```

**Verify network:**
```bash
# Test from dashboard container
docker-compose exec dashboard curl http://api:8080/health
```

### VictoriaMetrics

#### No Metrics Data

**Check:**

1. **Is VictoriaMetrics running?**
   ```bash
   docker-compose ps victoriametrics
   curl http://localhost:8428/health
   ```

2. **Are collectors sending data?**
   ```bash
   docker-compose logs collectors
   ```

3. **Check disk space**
   ```bash
   df -h
   ```

4. **Query metrics manually**
   ```bash
   curl 'http://localhost:8428/api/v1/query?query=up'
   ```

#### High Memory Usage

**Solutions:**

1. **Reduce retention**
   ```yaml
   # docker-compose.yml
   command:
     - "--retentionPeriod=1"  # 1 month instead of 12
   ```

2. **Enable deduplication**
   ```yaml
   command:
     - "--dedup.minScrapeInterval=30s"
   ```

3. **Limit cache**
   ```yaml
   command:
     - "--memory.allowedPercent=50"
   ```

### Loki

#### Logs Not Appearing

**Check:**

1. **Loki is running**
   ```bash
   curl http://localhost:3100/ready
   ```

2. **Check log ingestion**
   ```bash
   curl -G -s "http://localhost:3100/loki/api/v1/query" \
     --data-urlencode 'query={job="sentio"}' | jq
   ```

3. **Collectors are sending logs**
   ```bash
   docker-compose logs collectors | grep -i loki
   ```

#### Loki Out of Disk Space

**Solutions:**

1. **Reduce retention**
   ```yaml
   # config/loki-config.yml
   limits_config:
     retention_period: 168h  # 7 days instead of 31
   ```

2. **Enable compaction**
   ```yaml
   compactor:
     working_directory: /loki/compactor
     shared_store: filesystem
     retention_enabled: true
   ```

3. **Clean old data manually**
   ```bash
   docker-compose exec loki rm -rf /loki/chunks/*
   ```

### Collectors

#### Collectors Crash Repeatedly

**Check logs:**
```bash
docker-compose logs collectors
```

**Common causes:**

1. **Invalid configuration**
   - Validate `config/connectors.yml`
   - Check for syntax errors

2. **Network issues**
   ```bash
   # Test connectivity
   docker-compose exec collectors ping victoriametrics
   ```

3. **Memory limit**
   ```bash
   # Increase memory
   # docker-compose.yml
   deploy:
     resources:
       limits:
         memory: 1G
   ```

### Connectors

#### Devices Not Connecting

**Check:**

1. **Connector configuration**
   ```bash
   cat config/connectors.yml
   ```

2. **Network connectivity**
   ```bash
   # Test from connectors container
   docker-compose exec connectors ping <device-ip>
   docker-compose exec connectors curl http://<device-ip>
   ```

3. **Connector logs**
   ```bash
   docker-compose logs -f connectors
   ```

#### Home Assistant Connection Failed

**Check:**

1. **Home Assistant is accessible**
   ```bash
   curl http://homeassistant.local:8123/api/
   ```

2. **Token is valid**
   ```bash
   curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://homeassistant.local:8123/api/states
   ```

3. **Network configuration**
   - Make sure containers can reach Home Assistant
   - Check firewall rules

#### Modbus Connection Timeout

**Solutions:**

1. **Verify PLC IP and port**
   ```bash
   # Test TCP connection
   telnet <plc-ip> 502
   ```

2. **Check slave ID**
   - Must match PLC configuration
   - Usually 1 for single device

3. **Adjust timeout**
   ```yaml
   # config/connectors.yml
   modbus:
     timeout: 10  # Increase timeout
   ```

#### OPC-UA Security Error

**Solutions:**

1. **Use correct security policy**
   ```yaml
   opcua:
     security_policy: "None"  # Try without security first
     security_mode: "None"
   ```

2. **Certificate issues**
   ```bash
   # Generate certificates
   openssl req -x509 -newkey rsa:2048 \
     -keyout certs/client-key.pem \
     -out certs/client-cert.pem \
     -days 365 -nodes
   ```

3. **Trust server certificate**
   - Export server certificate
   - Add to trusted certificates

## Performance Issues

### Slow Query Response

**Solutions:**

1. **Check query complexity**
   - Simplify PromQL/LogQL queries
   - Reduce time range
   - Use recording rules

2. **Increase cache**
   ```yaml
   # For VictoriaMetrics
   command:
     - "--search.maxConcurrentRequests=16"
   ```

3. **Add more resources**
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '4'
         memory: 4G
   ```

### High CPU Usage

**Identify culprit:**
```bash
docker stats
```

**Solutions:**

1. **Reduce polling frequency**
   ```yaml
   # config/connectors.yml
   poll_interval: 60  # Increase from 30
   ```

2. **Limit concurrent requests**
3. **Scale horizontally**
   ```bash
   docker-compose up -d --scale collectors=2
   ```

### Disk Space Issues

**Check usage:**
```bash
du -sh data/*
df -h
```

**Solutions:**

1. **Reduce retention periods**
2. **Enable downsampling**
3. **Clean old data**
   ```bash
   # Remove old VictoriaMetrics data
   docker-compose stop victoriametrics
   rm -rf data/victoriametrics/data
   docker-compose start victoriametrics
   ```

## Network Issues

### Services Can't Communicate

**Check Docker network:**
```bash
# List networks
docker network ls

# Inspect network
docker network inspect sentio-iot_sentio-network

# Check container connectivity
docker-compose exec api ping postgres
docker-compose exec api ping victoriametrics
```

**Solution:**
```bash
# Recreate network
docker-compose down
docker-compose up -d
```

### Can't Access from Other Machines

**Check:**

1. **Firewall rules**
   ```bash
   # Ubuntu
   sudo ufw allow 3000
   sudo ufw allow 8080
   ```

2. **Bind to all interfaces**
   ```yaml
   # docker-compose.yml
   ports:
     - "0.0.0.0:8080:8080"  # Not just localhost
   ```

3. **Docker network mode**
   - Ensure not using `network_mode: "host"` incorrectly

## Data Issues

### Missing Historical Data

**Possible causes:**

1. **Retention period exceeded**
   - Check retention config
   - Data was automatically deleted

2. **Time sync issues**
   ```bash
   # Check system time
   date
   
   # Sync time
   sudo ntpdate pool.ntp.org
   ```

3. **Database corruption**
   - Check logs for errors
   - May need to restore from backup

### Duplicate Metrics

**Causes:**

1. **Multiple collectors**
   - Ensure only one collector per metric

2. **No deduplication**
   ```yaml
   # Enable in VictoriaMetrics
   command:
     - "--dedup.minScrapeInterval=30s"
   ```

### Incorrect Timestamps

**Solutions:**

1. **Sync system time**
   ```bash
   sudo ntpdate pool.ntp.org
   ```

2. **Check timezone**
   ```bash
   # Set timezone
   timedatectl set-timezone UTC
   ```

3. **Device time sync**
   - Ensure IoT devices have correct time

## Authentication Issues

### Can't Login

**Check:**

1. **Default credentials**
   - Username: `admin`
   - Password: `admin` (or from `.env`)

2. **Reset password**
   ```bash
   # Connect to database
   docker-compose exec postgres psql -U sentio -d sentio
   
   # Update password (hash of 'newpass')
   UPDATE users SET password_hash = '$2b$12$...' WHERE username = 'admin';
   ```

3. **Check JWT secret**
   ```bash
   # In .env
   JWT_SECRET_KEY=your-secret-key
   ```

### Token Expired

**Solution:**
```bash
# Increase expiration in .env
JWT_EXPIRE_MINUTES=1440  # 24 hours
```

**Or login again:**
```bash
curl -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'
```

## Upgrade Issues

### Upgrade Failed

**Safe upgrade process:**

```bash
# 1. Backup data
tar -czf backup-$(date +%Y%m%d).tar.gz data/

# 2. Pull latest changes
git pull origin main

# 3. Rebuild images
docker-compose build

# 4. Restart services
docker-compose up -d

# 5. Check logs
docker-compose logs -f
```

### Database Migration Failed

**Solution:**
```bash
# Check migration logs
docker-compose logs api | grep -i migration

# Manual migration
docker-compose exec postgres psql -U sentio -d sentio -f /path/to/migration.sql
```

## Still Having Issues?

### Collect Diagnostic Information

```bash
# Save diagnostic info
echo "=== System Info ===" > diagnostic.txt
uname -a >> diagnostic.txt
docker --version >> diagnostic.txt
docker-compose --version >> diagnostic.txt

echo "\n=== Services Status ===" >> diagnostic.txt
docker-compose ps >> diagnostic.txt

echo "\n=== Recent Logs ===" >> diagnostic.txt
docker-compose logs --tail=100 >> diagnostic.txt

echo "\n=== Resource Usage ===" >> diagnostic.txt
docker stats --no-stream >> diagnostic.txt
```

### Get Help

1. 🔍 [Search existing issues](https://github.com/NickScherbakov/sentio-iot/issues)
2. 📖 [Check FAQ](FAQ.md)
3. 💬 [Ask in Discussions](https://github.com/NickScherbakov/sentio-iot/discussions)
4. 🐛 [Report bug](https://github.com/NickScherbakov/sentio-iot/issues/new?template=bug_report.yml)

When reporting issues, include:
- System information
- Docker version
- Error messages
- Relevant logs
- Configuration (sanitized)
- Steps to reproduce

---

Last updated: November 2024
