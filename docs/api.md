# API Reference

Base URL: `http://localhost:8080/api/v1`

All API endpoints require authentication except `/auth/login` and `/health`.

## Authentication

### Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### Using the Token
Include the token in the Authorization header:
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## Health Check

### Get Health Status
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-09T08:00:00.000Z",
  "version": "1.0.0"
}
```

## Metrics

### Query Metrics
```http
POST /api/v1/metrics/query
Authorization: Bearer <token>
Content-Type: application/json

{
  "query": "up",
  "start": "2025-11-09T00:00:00Z",
  "end": "2025-11-09T12:00:00Z",
  "step": "15s"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "resultType": "matrix",
    "result": [
      {
        "metric": {
          "__name__": "up",
          "job": "sentio"
        },
        "values": [
          [1699488000, "1"],
          [1699488015, "1"]
        ]
      }
    ]
  }
}
```

### List Metric Series
```http
GET /api/v1/metrics/series
Authorization: Bearer <token>
```

**Response:**
```json
{
  "status": "success",
  "data": ["up", "cpu_usage", "memory_usage", "disk_usage"]
}
```

## Logs

### Query Logs
```http
POST /api/v1/logs/query
Authorization: Bearer <token>
Content-Type: application/json

{
  "query": "{job=\"sentio\"}",
  "start": "2025-11-09T00:00:00Z",
  "end": "2025-11-09T12:00:00Z",
  "limit": 100
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "resultType": "streams",
    "result": [
      {
        "stream": {
          "job": "sentio",
          "level": "info"
        },
        "values": [
          ["1699488000000000000", "Application started"],
          ["1699488015000000000", "Processing request"]
        ]
      }
    ]
  }
}
```

### List Log Labels
```http
GET /api/v1/logs/labels
Authorization: Bearer <token>
```

**Response:**
```json
{
  "status": "success",
  "data": ["job", "level", "service", "host"]
}
```

## Traces

### Query Traces
```http
POST /api/v1/traces/query
Authorization: Bearer <token>
Content-Type: application/json

{
  "service": "api",
  "operation": "GET /metrics",
  "start": "2025-11-09T00:00:00Z",
  "end": "2025-11-09T12:00:00Z",
  "limit": 50
}
```

**Response:**
```json
{
  "traces": [
    {
      "traceID": "abc123def456",
      "spanID": "span001",
      "operationName": "GET /metrics",
      "startTime": 1699488000,
      "duration": 125,
      "tags": {
        "http.method": "GET",
        "http.status_code": 200
      }
    }
  ]
}
```

### Get Trace by ID
```http
GET /api/v1/traces/{trace_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "traceID": "abc123def456",
  "spans": [
    {
      "spanID": "span001",
      "operationName": "GET /metrics",
      "startTime": 1699488000,
      "duration": 125,
      "references": []
    }
  ]
}
```

## Devices

### List Devices
```http
GET /api/v1/devices
Authorization: Bearer <token>
```

**Response:**
```json
{
  "devices": [
    {
      "id": "device-001",
      "name": "Temperature Sensor A",
      "type": "sensor",
      "protocol": "zigbee",
      "endpoint": "zigbee://00:12:4b:00:1c:a1:b2:c3",
      "metadata": {
        "location": "Room A"
      }
    }
  ]
}
```

### Get Device
```http
GET /api/v1/devices/{device_id}
Authorization: Bearer <token>
```

### Create Device
```http
POST /api/v1/devices
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Temperature Sensor B",
  "type": "sensor",
  "protocol": "modbus",
  "endpoint": "192.168.1.100:502",
  "metadata": {
    "location": "Room B",
    "unit_id": 1
  }
}
```

**Response:**
```json
{
  "id": "device-002",
  "name": "Temperature Sensor B",
  "type": "sensor",
  "protocol": "modbus",
  "endpoint": "192.168.1.100:502",
  "metadata": {
    "location": "Room B",
    "unit_id": 1
  }
}
```

### Update Device
```http
PUT /api/v1/devices/{device_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Updated Sensor Name",
  "type": "sensor",
  "protocol": "modbus",
  "endpoint": "192.168.1.100:502"
}
```

### Delete Device
```http
DELETE /api/v1/devices/{device_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "status": "deleted",
  "id": "device-002"
}
```

## Alerts

### List Alerts
```http
GET /api/v1/alerts
Authorization: Bearer <token>
```

**Response:**
```json
{
  "alerts": [
    {
      "id": "alert-001",
      "name": "High CPU Usage",
      "description": "CPU usage above 80%",
      "query": "cpu_usage > 80",
      "threshold": 80,
      "severity": "high",
      "enabled": true
    }
  ]
}
```

### Get Alert
```http
GET /api/v1/alerts/{alert_id}
Authorization: Bearer <token>
```

### Create Alert
```http
POST /api/v1/alerts
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "High Memory Usage",
  "description": "Memory usage above 90%",
  "query": "memory_usage > 90",
  "threshold": 90,
  "severity": "critical",
  "enabled": true
}
```

**Response:**
```json
{
  "id": "alert-002",
  "name": "High Memory Usage",
  "description": "Memory usage above 90%",
  "query": "memory_usage > 90",
  "threshold": 90,
  "severity": "critical",
  "enabled": true
}
```

### Update Alert
```http
PUT /api/v1/alerts/{alert_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Updated Alert Name",
  "threshold": 95
}
```

### Delete Alert
```http
DELETE /api/v1/alerts/{alert_id}
Authorization: Bearer <token>
```

## AI Insights

### Get Anomalies
```http
GET /api/v1/ai/anomalies
Authorization: Bearer <token>
```

**Response:**
```json
{
  "anomalies": [
    {
      "timestamp": "2025-11-09T08:30:00Z",
      "metric": "cpu_usage",
      "value": 95.5,
      "score": -0.85
    }
  ]
}
```

### Get Predictions
```http
GET /api/v1/ai/predictions
Authorization: Bearer <token>
```

**Response:**
```json
{
  "predictions": [
    {
      "device_id": "device-001",
      "risk_level": "high",
      "confidence": 0.85,
      "estimated_time_to_failure": "1-3 days",
      "indicators": {
        "volatility": 0.6,
        "trend": -0.15
      }
    }
  ]
}
```

## System Status

### Get Platform Status
```http
GET /api/v1/status
Authorization: Bearer <token>
```

**Response:**
```json
{
  "status": "operational",
  "components": {
    "api": "healthy",
    "metrics": "healthy",
    "logs": "healthy",
    "traces": "healthy",
    "ai_engine": "healthy"
  },
  "timestamp": "2025-11-09T08:00:00Z"
}
```

## WebSocket

### Real-time Updates
```javascript
const ws = new WebSocket('ws://localhost:8080/ws');

ws.onopen = () => {
  console.log('Connected');
};

ws.onmessage = (event) => {
  console.log('Message:', event.data);
};

ws.onerror = (error) => {
  console.error('Error:', error);
};

ws.onclose = () => {
  console.log('Disconnected');
};
```

## Error Responses

All endpoints may return these error responses:

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

API endpoints are rate-limited to:
- 1000 requests per minute per IP
- 10000 requests per hour per IP

Rate limit headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 995
X-RateLimit-Reset: 1699488060
```

## Pagination

List endpoints support pagination:

```http
GET /api/v1/devices?page=2&per_page=20
```

Response includes pagination metadata:
```json
{
  "devices": [...],
  "pagination": {
    "page": 2,
    "per_page": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

## OpenAPI/Swagger Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`
