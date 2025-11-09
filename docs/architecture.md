# Architecture Overview

## System Design

Sentio IoT is designed as a distributed, microservices-based observability platform optimized for IoT and edge computing environments.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          Users / Operators                       │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
                   ┌────────────────┐
                   │   Dashboard    │
                   │    (React)     │
                   └────────┬───────┘
                            │ HTTPS/WSS
                            ▼
┌───────────────────────────────────────────────────────────────────┐
│                        API Gateway Layer                          │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              API Server (FastAPI)                        │   │
│  │  - REST API Endpoints                                    │   │
│  │  - WebSocket Server                                      │   │
│  │  - Authentication & Authorization                        │   │
│  │  - Request Routing                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐   ┌──────────────┐   ┌─────────────┐
│   Collectors  │   │  Connectors  │   │  AI Engine  │
│   Service     │   │   Service    │   │             │
└───────┬───────┘   └──────┬───────┘   └──────┬──────┘
        │                  │                   │
        │                  │                   │
        ▼                  ▼                   ▼
┌───────────────────────────────────────────────────────┐
│              Data Storage Layer                        │
│                                                        │
│  ┌──────────────┐  ┌──────────┐  ┌──────────────┐  │
│  │VictoriaMetrics│  │  Loki    │  │    Tempo     │  │
│  │  (Metrics)   │  │  (Logs)  │  │  (Traces)    │  │
│  └──────────────┘  └──────────┘  └──────────────┘  │
│                                                        │
│  ┌──────────────┐  ┌──────────┐                     │
│  │  PostgreSQL  │  │  Redis   │                     │
│  │  (Metadata)  │  │ (Cache)  │                     │
│  └──────────────┘  └──────────┘                     │
└───────────────────────────────────────────────────────┘
                        ▲
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│Home Assistant│ │    Zigbee    │ │   Modbus     │
│              │ │   Devices    │ │   OPC-UA     │
└──────────────┘ └──────────────┘ └──────────────┘
```

## Component Details

### 1. Dashboard (Frontend)

**Technology:** React 18 + Material-UI + Vite

**Responsibilities:**
- User interface for monitoring and management
- Real-time data visualization
- Query builder for metrics, logs, and traces
- Alert and device management
- WebSocket client for live updates

**Key Features:**
- Responsive design for desktop and mobile
- Dark mode optimized
- Real-time charts using Recharts
- Optimized bundle with code splitting

### 2. API Server

**Technology:** FastAPI + Python 3.11

**Responsibilities:**
- REST API endpoints for all operations
- WebSocket server for real-time streaming
- JWT-based authentication
- Request validation and authorization
- Query routing to storage backends
- Business logic coordination

**Key Features:**
- Async/await for high concurrency
- Automatic OpenAPI documentation
- Type hints with Pydantic models
- CORS configuration
- Rate limiting ready

### 3. Collectors Service

**Technology:** Python 3.11 + aiohttp + OpenTelemetry

**Responsibilities:**
- Receive metrics, logs, and traces from devices/connectors
- Buffer and batch data for efficiency
- Forward to appropriate storage backends
- Metric exposition in Prometheus format

**Key Features:**
- High-throughput ingestion (100k+ metrics/sec)
- Automatic batching and flushing
- OpenTelemetry integration for traces
- Prometheus metrics for self-monitoring

### 4. Connectors Service

**Technology:** Python 3.11 + Protocol Libraries

**Responsibilities:**
- Protocol-specific device communication
- Data normalization and transformation
- Periodic polling or event-based collection
- Send normalized data to collectors

**Supported Protocols:**
- **Home Assistant**: REST API integration
- **Zigbee**: MQTT via Zigbee2MQTT
- **Modbus**: Modbus TCP with pymodbus
- **OPC-UA**: Industrial protocol with opcua library

**Key Features:**
- Configurable polling intervals
- Error handling and retry logic
- Extensible connector framework

### 5. AI Engine

**Technology:** Python 3.11 + scikit-learn + TensorFlow

**Responsibilities:**
- Anomaly detection on metrics
- Predictive maintenance modeling
- Intelligent alert generation
- Model training and updating

**Algorithms:**
- **Anomaly Detection**: Isolation Forest
- **Trend Analysis**: Linear regression
- **Time Series**: Prophet (planned)
- **Deep Learning**: LSTM (planned)

**Key Features:**
- Automatic model retraining
- Configurable thresholds
- Alert cooldown and deduplication
- Results caching in Redis

### 6. Storage Layer

#### VictoriaMetrics
- **Purpose**: Time-series metrics storage
- **Features**: High compression, fast queries, PromQL compatible
- **Retention**: Configurable (default: 12 months)
- **Scalability**: Can be clustered for high availability

#### Loki
- **Purpose**: Log aggregation and storage
- **Features**: Label-based indexing, LogQL queries
- **Retention**: Configurable (default: 31 days)
- **Integration**: Compatible with Grafana

#### Tempo
- **Purpose**: Distributed tracing storage
- **Features**: OpenTelemetry compatible, S3/GCS backends
- **Retention**: Configurable (default: 7 days)
- **Integration**: Trace visualization and analysis

#### PostgreSQL
- **Purpose**: Metadata storage
- **Data**: Users, devices, alerts, configurations
- **Features**: ACID compliance, relational queries
- **Backup**: Regular automated backups recommended

#### Redis
- **Purpose**: Caching and message queue
- **Use Cases**: Session storage, alert cooldowns, temporary data
- **Features**: In-memory performance, persistence options

## Data Flow

### Metrics Flow
```
Device → Connector → Collector → VictoriaMetrics → API → Dashboard
                                      ↓
                                  AI Engine (analyze)
                                      ↓
                                  Anomalies/Predictions
```

### Logs Flow
```
Device → Connector → Collector → Loki → API → Dashboard
```

### Traces Flow
```
Device → OpenTelemetry → Tempo → API → Dashboard
```

## Communication Patterns

### Synchronous (REST)
- Dashboard ↔ API Server
- API Server ↔ Storage Backends
- Connectors → Collectors

### Asynchronous (WebSocket)
- Dashboard ↔ API Server (real-time updates)

### Event-Driven (MQTT)
- Zigbee Devices → MQTT Broker → Connector

### Polling
- Connectors → Devices (Modbus, OPC-UA, Home Assistant)

## Scalability

### Horizontal Scaling
- **API Server**: Multiple instances behind load balancer
- **Collectors**: Stateless, can scale independently
- **Connectors**: Distributed by protocol/device group

### Vertical Scaling
- VictoriaMetrics: Increase resources for larger datasets
- PostgreSQL: Upgrade instance for more metadata
- Redis: Add memory for larger cache

### Data Sharding
- Metrics: By device ID or label
- Logs: By service or time range
- Traces: By service name

## Security Architecture

### Authentication Flow
```
1. User → Dashboard: Login credentials
2. Dashboard → API: POST /auth/login
3. API: Validate credentials
4. API → Dashboard: JWT token
5. Dashboard: Store token (localStorage)
6. Dashboard → API: Requests with Bearer token
7. API: Validate JWT, process request
```

### Network Security
- TLS/HTTPS for external communication
- mTLS for service-to-service (optional)
- Network policies for container isolation
- Firewall rules for port restrictions

### Data Security
- Encrypted environment variables
- Secrets management (external vault recommended)
- Database encryption at rest
- Audit logging for access

## Performance Optimization

### Frontend
- Code splitting and lazy loading
- Asset compression (gzip/brotli)
- CDN for static assets
- Service worker for offline capability

### Backend
- Connection pooling (database, HTTP)
- Response caching (Redis)
- Async I/O throughout
- Batch processing for writes

### Storage
- Appropriate retention policies
- Index optimization
- Compression enabled
- Regular vacuuming/compaction

## Monitoring & Observability

### Self-Monitoring
- Prometheus metrics from all services
- Health check endpoints
- Structured logging with correlation IDs
- Distributed tracing for requests

### Key Metrics
- Request latency (p50, p95, p99)
- Throughput (requests/sec, data points/sec)
- Error rates
- Resource utilization (CPU, memory, disk)
- Queue depths

## Deployment Topologies

### Development
- Single host with Docker Compose
- All services on same network
- Local storage volumes

### Production (Single Region)
- Load-balanced API servers
- Replicated storage backends
- Separate networks for services
- Persistent volumes for data

### Multi-Region (Future)
- Regional deployments
- Cross-region replication
- Geo-distributed storage
- Edge collectors

## Technology Choices

### Why FastAPI?
- High performance (Starlette + Pydantic)
- Automatic API documentation
- Type safety with Python type hints
- Async/await support

### Why VictoriaMetrics?
- Better performance than Prometheus
- Lower resource usage
- Compatible with Prometheus ecosystem
- Built-in downsampling

### Why React?
- Component-based architecture
- Large ecosystem
- Performance optimizations
- Strong community support

### Why Python for Services?
- Rich library ecosystem
- Great for data processing
- ML/AI libraries available
- Readable and maintainable

## Future Enhancements

### Planned Features
- Kubernetes native deployment
- Multi-tenancy support
- Plugin system for custom connectors
- Mobile application
- Enhanced ML models
- Auto-scaling based on load
- Cross-region failover
- GraphQL API option

### Performance Improvements
- Query result caching
- Materialized views
- Read replicas
- Write-ahead logging optimization

### Security Enhancements
- OAuth2/OIDC integration
- Fine-grained RBAC
- Audit log encryption
- Secret rotation automation
