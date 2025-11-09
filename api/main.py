"""
Sentio IoT API Server
Main application entry point for the distributed observability platform
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import httpx
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from pydantic import BaseModel, Field

from config import settings
from auth import get_current_user, create_access_token
from database import engine, Base, get_db
from websocket_manager import ConnectionManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Lifecycle management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Starting Sentio IoT API Server")
    # Create database tables
    Base.metadata.create_all(bind=engine)
    yield
    logger.info("Shutting down Sentio IoT API Server")


# Initialize FastAPI app
app = FastAPI(
    title="Sentio IoT API",
    description="Distributed Observability Platform for IoT and Edge Devices",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager
ws_manager = ConnectionManager()


# Pydantic models
class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MetricsQuery(BaseModel):
    query: str
    start: Optional[datetime] = Field(default_factory=lambda: datetime.utcnow() - timedelta(hours=1))
    end: Optional[datetime] = Field(default_factory=datetime.utcnow)
    step: Optional[str] = "15s"


class LogsQuery(BaseModel):
    query: str
    start: Optional[datetime] = Field(default_factory=lambda: datetime.utcnow() - timedelta(hours=1))
    end: Optional[datetime] = Field(default_factory=datetime.utcnow)
    limit: Optional[int] = 100


class TracesQuery(BaseModel):
    service: Optional[str] = None
    operation: Optional[str] = None
    start: Optional[datetime] = Field(default_factory=lambda: datetime.utcnow() - timedelta(hours=1))
    end: Optional[datetime] = Field(default_factory=datetime.utcnow)
    limit: Optional[int] = 50


class Alert(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    query: str
    threshold: float
    severity: str = "warning"
    enabled: bool = True


class Device(BaseModel):
    id: Optional[str] = None
    name: str
    type: str
    protocol: str
    endpoint: str
    metadata: Optional[Dict[str, Any]] = None


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


# Authentication endpoints
@app.post("/api/v1/auth/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """Authenticate user and return JWT token"""
    # TODO: Implement proper user authentication with database
    # This is a simplified version for demo purposes
    if request.username == "admin" and request.password == "admin":
        access_token = create_access_token(data={"sub": request.username})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


# Metrics endpoints
@app.post("/api/v1/metrics/query")
async def query_metrics(query: MetricsQuery, current_user: dict = Depends(get_current_user)):
    """Query metrics from VictoriaMetrics"""
    try:
        async with httpx.AsyncClient() as client:
            params = {
                "query": query.query,
                "start": int(query.start.timestamp()),
                "end": int(query.end.timestamp()),
                "step": query.step
            }
            response = await client.get(
                f"{settings.VICTORIAMETRICS_URL}/api/v1/query_range",
                params=params,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Error querying metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/metrics/series")
async def list_metric_series(current_user: dict = Depends(get_current_user)):
    """List available metric series"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.VICTORIAMETRICS_URL}/api/v1/label/__name__/values",
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Error listing metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Logs endpoints
@app.post("/api/v1/logs/query")
async def query_logs(query: LogsQuery, current_user: dict = Depends(get_current_user)):
    """Query logs from Loki"""
    try:
        async with httpx.AsyncClient() as client:
            params = {
                "query": query.query,
                "start": int(query.start.timestamp() * 1e9),
                "end": int(query.end.timestamp() * 1e9),
                "limit": query.limit
            }
            response = await client.get(
                f"{settings.LOKI_URL}/loki/api/v1/query_range",
                params=params,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Error querying logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/logs/labels")
async def list_log_labels(current_user: dict = Depends(get_current_user)):
    """List available log labels"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.LOKI_URL}/loki/api/v1/labels",
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Error listing log labels: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Traces endpoints
@app.post("/api/v1/traces/query")
async def query_traces(query: TracesQuery, current_user: dict = Depends(get_current_user)):
    """Query traces from Tempo"""
    try:
        async with httpx.AsyncClient() as client:
            params = {
                "start": int(query.start.timestamp()),
                "end": int(query.end.timestamp()),
                "limit": query.limit
            }
            if query.service:
                params["service"] = query.service
            if query.operation:
                params["operation"] = query.operation
            
            response = await client.get(
                f"{settings.TEMPO_URL}/api/search",
                params=params,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Error querying traces: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/traces/{trace_id}")
async def get_trace(trace_id: str, current_user: dict = Depends(get_current_user)):
    """Get specific trace by ID"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.TEMPO_URL}/api/traces/{trace_id}",
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Error getting trace: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Alerts endpoints
@app.get("/api/v1/alerts")
async def list_alerts(current_user: dict = Depends(get_current_user)):
    """List all configured alerts"""
    # TODO: Implement database storage for alerts
    return {"alerts": []}


@app.post("/api/v1/alerts")
async def create_alert(alert: Alert, current_user: dict = Depends(get_current_user)):
    """Create a new alert rule"""
    # TODO: Implement alert creation in database
    return {"id": "alert-001", **alert.dict()}


@app.get("/api/v1/alerts/{alert_id}")
async def get_alert(alert_id: str, current_user: dict = Depends(get_current_user)):
    """Get specific alert by ID"""
    # TODO: Implement alert retrieval from database
    raise HTTPException(status_code=404, detail="Alert not found")


@app.put("/api/v1/alerts/{alert_id}")
async def update_alert(alert_id: str, alert: Alert, current_user: dict = Depends(get_current_user)):
    """Update an existing alert"""
    # TODO: Implement alert update in database
    return {"id": alert_id, **alert.dict()}


@app.delete("/api/v1/alerts/{alert_id}")
async def delete_alert(alert_id: str, current_user: dict = Depends(get_current_user)):
    """Delete an alert"""
    # TODO: Implement alert deletion from database
    return {"status": "deleted", "id": alert_id}


# Devices endpoints
@app.get("/api/v1/devices")
async def list_devices(current_user: dict = Depends(get_current_user)):
    """List all registered devices"""
    # TODO: Implement database storage for devices
    return {"devices": []}


@app.post("/api/v1/devices")
async def register_device(device: Device, current_user: dict = Depends(get_current_user)):
    """Register a new device"""
    # TODO: Implement device registration in database
    return {"id": "device-001", **device.dict()}


@app.get("/api/v1/devices/{device_id}")
async def get_device(device_id: str, current_user: dict = Depends(get_current_user)):
    """Get specific device by ID"""
    # TODO: Implement device retrieval from database
    raise HTTPException(status_code=404, detail="Device not found")


@app.put("/api/v1/devices/{device_id}")
async def update_device(device_id: str, device: Device, current_user: dict = Depends(get_current_user)):
    """Update a device"""
    # TODO: Implement device update in database
    return {"id": device_id, **device.dict()}


@app.delete("/api/v1/devices/{device_id}")
async def delete_device(device_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a device"""
    # TODO: Implement device deletion from database
    return {"status": "deleted", "id": device_id}


# AI Insights endpoints
@app.get("/api/v1/ai/anomalies")
async def get_anomalies(current_user: dict = Depends(get_current_user)):
    """Get detected anomalies from AI engine"""
    # TODO: Implement AI engine integration
    return {"anomalies": []}


@app.get("/api/v1/ai/predictions")
async def get_predictions(current_user: dict = Depends(get_current_user)):
    """Get fault predictions from AI engine"""
    # TODO: Implement AI engine integration
    return {"predictions": []}


# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time data streaming"""
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back for now, implement real streaming later
            await ws_manager.send_personal_message(f"Echo: {data}", websocket)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)


# Status endpoint
@app.get("/api/v1/status")
async def get_status(current_user: dict = Depends(get_current_user)):
    """Get platform status"""
    return {
        "status": "operational",
        "components": {
            "api": "healthy",
            "metrics": "healthy",
            "logs": "healthy",
            "traces": "healthy",
            "ai_engine": "healthy"
        },
        "timestamp": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
