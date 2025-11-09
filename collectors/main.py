"""
Sentio IoT Collectors Service
Handles metrics, logs, and traces collection from devices
"""
import os
import time
import logging
from datetime import datetime
from aiohttp import web
from prometheus_client import Counter, Gauge, Histogram, generate_latest
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
import asyncio
import json
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
VICTORIAMETRICS_URL = os.getenv('VICTORIAMETRICS_URL', 'http://victoriametrics:8428')
LOKI_URL = os.getenv('LOKI_URL', 'http://loki:3100')
TEMPO_URL = os.getenv('TEMPO_URL', 'http://tempo:3200')

# Initialize OpenTelemetry
resource = Resource.create({"service.name": "sentio-collectors"})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# Configure OTLP exporter
otlp_exporter = OTLPSpanExporter(endpoint=f"{TEMPO_URL.replace('http://', '')}:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Prometheus metrics
metrics_received = Counter('sentio_metrics_received_total', 'Total metrics received')
logs_received = Counter('sentio_logs_received_total', 'Total logs received')
traces_received = Counter('sentio_traces_received_total', 'Total traces received')
collection_errors = Counter('sentio_collection_errors_total', 'Total collection errors')
collection_duration = Histogram('sentio_collection_duration_seconds', 'Collection duration')


class MetricsCollector:
    """Collects and forwards metrics to VictoriaMetrics"""
    
    def __init__(self):
        self.buffer = []
        self.buffer_size = 1000
        self.flush_interval = 10  # seconds
    
    async def collect_metric(self, metric_data: dict):
        """Collect a single metric"""
        try:
            self.buffer.append(metric_data)
            metrics_received.inc()
            
            if len(self.buffer) >= self.buffer_size:
                await self.flush()
        except Exception as e:
            logger.error(f"Error collecting metric: {e}")
            collection_errors.inc()
    
    async def flush(self):
        """Flush metrics buffer to VictoriaMetrics"""
        if not self.buffer:
            return
        
        try:
            # Convert to Prometheus exposition format
            lines = []
            for metric in self.buffer:
                name = metric.get('name', 'unknown')
                value = metric.get('value', 0)
                labels = metric.get('labels', {})
                timestamp = metric.get('timestamp', int(time.time() * 1000))
                
                label_str = ','.join([f'{k}="{v}"' for k, v in labels.items()])
                if label_str:
                    line = f"{name}{{{label_str}}} {value} {timestamp}"
                else:
                    line = f"{name} {value} {timestamp}"
                lines.append(line)
            
            # Send to VictoriaMetrics
            data = '\n'.join(lines)
            response = requests.post(
                f"{VICTORIAMETRICS_URL}/api/v1/import/prometheus",
                data=data.encode('utf-8'),
                headers={'Content-Type': 'text/plain'},
                timeout=10
            )
            response.raise_for_status()
            
            logger.info(f"Flushed {len(self.buffer)} metrics to VictoriaMetrics")
            self.buffer = []
        except Exception as e:
            logger.error(f"Error flushing metrics: {e}")
            collection_errors.inc()
    
    async def start_flush_loop(self):
        """Periodically flush metrics buffer"""
        while True:
            await asyncio.sleep(self.flush_interval)
            await self.flush()


class LogsCollector:
    """Collects and forwards logs to Loki"""
    
    def __init__(self):
        self.buffer = []
        self.buffer_size = 100
        self.flush_interval = 5  # seconds
    
    async def collect_log(self, log_data: dict):
        """Collect a single log entry"""
        try:
            self.buffer.append(log_data)
            logs_received.inc()
            
            if len(self.buffer) >= self.buffer_size:
                await self.flush()
        except Exception as e:
            logger.error(f"Error collecting log: {e}")
            collection_errors.inc()
    
    async def flush(self):
        """Flush logs buffer to Loki"""
        if not self.buffer:
            return
        
        try:
            # Format logs for Loki
            streams = {}
            for log in self.buffer:
                labels = log.get('labels', {})
                label_str = '{' + ','.join([f'{k}="{v}"' for k, v in labels.items()]) + '}'
                
                if label_str not in streams:
                    streams[label_str] = []
                
                timestamp_ns = str(log.get('timestamp', int(time.time() * 1e9)))
                line = log.get('message', '')
                streams[label_str].append([timestamp_ns, line])
            
            # Convert to Loki format
            loki_streams = []
            for labels, values in streams.items():
                loki_streams.append({
                    "stream": json.loads(labels.replace("'", '"')),
                    "values": values
                })
            
            payload = {"streams": loki_streams}
            
            # Send to Loki
            response = requests.post(
                f"{LOKI_URL}/loki/api/v1/push",
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            response.raise_for_status()
            
            logger.info(f"Flushed {len(self.buffer)} logs to Loki")
            self.buffer = []
        except Exception as e:
            logger.error(f"Error flushing logs: {e}")
            collection_errors.inc()
    
    async def start_flush_loop(self):
        """Periodically flush logs buffer"""
        while True:
            await asyncio.sleep(self.flush_interval)
            await self.flush()


class TracesCollector:
    """Collects and forwards traces to Tempo"""
    
    def __init__(self):
        pass
    
    async def collect_trace(self, trace_data: dict):
        """Collect a trace span"""
        try:
            traces_received.inc()
            # OpenTelemetry SDK handles trace export automatically
            # This is a placeholder for additional trace processing if needed
        except Exception as e:
            logger.error(f"Error collecting trace: {e}")
            collection_errors.inc()


# Initialize collectors
metrics_collector = MetricsCollector()
logs_collector = LogsCollector()
traces_collector = TracesCollector()


# HTTP handlers
async def handle_metrics(request):
    """Handle incoming metrics"""
    try:
        data = await request.json()
        await metrics_collector.collect_metric(data)
        return web.json_response({"status": "ok"})
    except Exception as e:
        logger.error(f"Error handling metrics: {e}")
        return web.json_response({"error": str(e)}, status=500)


async def handle_logs(request):
    """Handle incoming logs"""
    try:
        data = await request.json()
        await logs_collector.collect_log(data)
        return web.json_response({"status": "ok"})
    except Exception as e:
        logger.error(f"Error handling logs: {e}")
        return web.json_response({"error": str(e)}, status=500)


async def handle_traces(request):
    """Handle incoming traces"""
    try:
        data = await request.json()
        await traces_collector.collect_trace(data)
        return web.json_response({"status": "ok"})
    except Exception as e:
        logger.error(f"Error handling traces: {e}")
        return web.json_response({"error": str(e)}, status=500)


async def handle_prometheus_metrics(request):
    """Expose Prometheus metrics"""
    return web.Response(text=generate_latest().decode('utf-8'), content_type='text/plain')


async def handle_health(request):
    """Health check endpoint"""
    return web.json_response({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    })


async def start_background_tasks(app):
    """Start background flush tasks"""
    app['metrics_flush_task'] = asyncio.create_task(metrics_collector.start_flush_loop())
    app['logs_flush_task'] = asyncio.create_task(logs_collector.start_flush_loop())


async def cleanup_background_tasks(app):
    """Cleanup background tasks"""
    app['metrics_flush_task'].cancel()
    app['logs_flush_task'].cancel()
    
    await app['metrics_flush_task']
    await app['logs_flush_task']


def create_app():
    """Create and configure the application"""
    app = web.Application()
    
    # Routes
    app.router.add_post('/collect/metrics', handle_metrics)
    app.router.add_post('/collect/logs', handle_logs)
    app.router.add_post('/collect/traces', handle_traces)
    app.router.add_get('/metrics', handle_prometheus_metrics)
    app.router.add_get('/health', handle_health)
    
    # Startup/cleanup
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    
    return app


if __name__ == '__main__':
    logger.info("Starting Sentio IoT Collectors Service")
    app = create_app()
    web.run_app(app, host='0.0.0.0', port=8081)
