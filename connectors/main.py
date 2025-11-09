"""
Sentio IoT Protocol Connectors
Integrates with Home Assistant, Zigbee, Modbus, and OPC-UA devices
"""
import os
import asyncio
import logging
from typing import Dict, Any, Optional
import yaml
import requests
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
COLLECTORS_URL = os.getenv('COLLECTORS_URL', 'http://collectors:8081')
CONFIG_PATH = os.getenv('CONFIG_PATH', '/app/config/connectors.yml')


class BaseConnector:
    """Base class for protocol connectors"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.enabled = config.get('enabled', True)
        self.poll_interval = config.get('poll_interval', 60)
    
    async def start(self):
        """Start the connector"""
        if not self.enabled:
            logger.info(f"{self.name} connector is disabled")
            return
        
        logger.info(f"Starting {self.name} connector")
        while True:
            try:
                await self.collect()
            except Exception as e:
                logger.error(f"Error in {self.name} connector: {e}")
            
            await asyncio.sleep(self.poll_interval)
    
    async def collect(self):
        """Collect data from the protocol - to be implemented by subclasses"""
        raise NotImplementedError
    
    async def send_metric(self, name: str, value: float, labels: Dict[str, str] = None):
        """Send metric to collectors"""
        try:
            metric = {
                'name': name,
                'value': value,
                'labels': labels or {},
                'timestamp': int(datetime.utcnow().timestamp() * 1000)
            }
            response = requests.post(
                f"{COLLECTORS_URL}/collect/metrics",
                json=metric,
                timeout=5
            )
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Error sending metric: {e}")
    
    async def send_log(self, message: str, labels: Dict[str, str] = None):
        """Send log to collectors"""
        try:
            log = {
                'message': message,
                'labels': labels or {},
                'timestamp': int(datetime.utcnow().timestamp() * 1e9)
            }
            response = requests.post(
                f"{COLLECTORS_URL}/collect/logs",
                json=log,
                timeout=5
            )
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Error sending log: {e}")


class HomeAssistantConnector(BaseConnector):
    """Home Assistant integration connector"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("HomeAssistant", config)
        self.base_url = config.get('url', 'http://homeassistant:8123')
        self.token = config.get('token', '')
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
    
    async def collect(self):
        """Collect data from Home Assistant"""
        try:
            # Get all states
            response = requests.get(
                f"{self.base_url}/api/states",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            states = response.json()
            logger.info(f"Retrieved {len(states)} entities from Home Assistant")
            
            # Process each entity
            for entity in states:
                entity_id = entity.get('entity_id', '')
                state = entity.get('state', '')
                attributes = entity.get('attributes', {})
                
                # Extract numeric values and send as metrics
                if self._is_numeric(state):
                    await self.send_metric(
                        'homeassistant_entity_state',
                        float(state),
                        {
                            'entity_id': entity_id,
                            'domain': entity_id.split('.')[0],
                            'friendly_name': attributes.get('friendly_name', entity_id)
                        }
                    )
                
                # Send log entry for state changes
                await self.send_log(
                    f"Entity {entity_id} state: {state}",
                    {
                        'connector': 'homeassistant',
                        'entity_id': entity_id,
                        'level': 'info'
                    }
                )
        
        except Exception as e:
            logger.error(f"Error collecting from Home Assistant: {e}")
    
    @staticmethod
    def _is_numeric(value: str) -> bool:
        """Check if a value is numeric"""
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False


class ModbusConnector(BaseConnector):
    """Modbus protocol connector"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("Modbus", config)
        self.host = config.get('host', 'localhost')
        self.port = config.get('port', 502)
        self.unit_id = config.get('unit_id', 1)
        self.registers = config.get('registers', [])
    
    async def collect(self):
        """Collect data from Modbus devices"""
        try:
            from pymodbus.client import ModbusTcpClient
            
            client = ModbusTcpClient(self.host, port=self.port)
            if not client.connect():
                logger.error(f"Failed to connect to Modbus device at {self.host}:{self.port}")
                return
            
            logger.info(f"Connected to Modbus device at {self.host}:{self.port}")
            
            # Read configured registers
            for register in self.registers:
                address = register.get('address', 0)
                count = register.get('count', 1)
                name = register.get('name', f'register_{address}')
                reg_type = register.get('type', 'holding')
                
                # Read register based on type
                if reg_type == 'holding':
                    result = client.read_holding_registers(address, count, unit=self.unit_id)
                elif reg_type == 'input':
                    result = client.read_input_registers(address, count, unit=self.unit_id)
                elif reg_type == 'coil':
                    result = client.read_coils(address, count, unit=self.unit_id)
                else:
                    continue
                
                if not result.isError():
                    if hasattr(result, 'registers'):
                        values = result.registers
                    elif hasattr(result, 'bits'):
                        values = result.bits
                    else:
                        continue
                    
                    # Send metrics
                    for i, value in enumerate(values[:count]):
                        await self.send_metric(
                            f'modbus_{name}',
                            float(value),
                            {
                                'host': self.host,
                                'port': str(self.port),
                                'address': str(address + i),
                                'type': reg_type
                            }
                        )
            
            client.close()
            
        except Exception as e:
            logger.error(f"Error collecting from Modbus: {e}")


class ZigbeeConnector(BaseConnector):
    """Zigbee protocol connector"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("Zigbee", config)
        self.mqtt_broker = config.get('mqtt_broker', 'localhost')
        self.mqtt_port = config.get('mqtt_port', 1883)
        self.mqtt_topic = config.get('mqtt_topic', 'zigbee2mqtt/#')
    
    async def collect(self):
        """Collect data from Zigbee devices via MQTT"""
        try:
            import asyncio_mqtt as aiomqtt
            
            async with aiomqtt.Client(self.mqtt_broker, self.mqtt_port) as client:
                await client.subscribe(self.mqtt_topic)
                logger.info(f"Subscribed to Zigbee MQTT topic: {self.mqtt_topic}")
                
                async for message in client.messages:
                    try:
                        import json
                        payload = json.loads(message.payload.decode())
                        topic = str(message.topic)
                        
                        # Extract device name from topic
                        device_name = topic.split('/')[-1]
                        
                        # Process numeric values
                        for key, value in payload.items():
                            if isinstance(value, (int, float)):
                                await self.send_metric(
                                    f'zigbee_{key}',
                                    float(value),
                                    {
                                        'device': device_name,
                                        'topic': topic
                                    }
                                )
                        
                        # Send log
                        await self.send_log(
                            f"Zigbee device {device_name} update: {json.dumps(payload)}",
                            {
                                'connector': 'zigbee',
                                'device': device_name,
                                'level': 'info'
                            }
                        )
                    
                    except Exception as e:
                        logger.error(f"Error processing Zigbee message: {e}")
        
        except Exception as e:
            logger.error(f"Error with Zigbee connector: {e}")


class OPCUAConnector(BaseConnector):
    """OPC-UA (Industrial Ethernet) connector"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("OPC-UA", config)
        self.endpoint = config.get('endpoint', 'opc.tcp://localhost:4840')
        self.nodes = config.get('nodes', [])
    
    async def collect(self):
        """Collect data from OPC-UA servers"""
        try:
            from opcua import Client
            
            client = Client(self.endpoint)
            client.connect()
            logger.info(f"Connected to OPC-UA server at {self.endpoint}")
            
            # Read configured nodes
            for node_config in self.nodes:
                node_id = node_config.get('id', '')
                name = node_config.get('name', node_id)
                
                try:
                    node = client.get_node(node_id)
                    value = node.get_value()
                    
                    if isinstance(value, (int, float)):
                        await self.send_metric(
                            f'opcua_{name}',
                            float(value),
                            {
                                'endpoint': self.endpoint,
                                'node_id': node_id
                            }
                        )
                    
                    await self.send_log(
                        f"OPC-UA node {name} value: {value}",
                        {
                            'connector': 'opcua',
                            'node_id': node_id,
                            'level': 'info'
                        }
                    )
                
                except Exception as e:
                    logger.error(f"Error reading OPC-UA node {node_id}: {e}")
            
            client.disconnect()
        
        except Exception as e:
            logger.error(f"Error with OPC-UA connector: {e}")


async def load_config() -> Dict[str, Any]:
    """Load connector configuration from file"""
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                return yaml.safe_load(f)
        else:
            logger.warning(f"Config file not found: {CONFIG_PATH}")
            return {}
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        return {}


async def main():
    """Main entry point"""
    logger.info("Starting Sentio IoT Protocol Connectors")
    
    # Load configuration
    config = await load_config()
    
    # Initialize connectors
    connectors = []
    
    # Home Assistant
    if 'homeassistant' in config:
        connectors.append(HomeAssistantConnector(config['homeassistant']))
    
    # Modbus
    if 'modbus' in config:
        for modbus_config in config.get('modbus', []):
            connectors.append(ModbusConnector(modbus_config))
    
    # Zigbee
    if 'zigbee' in config:
        connectors.append(ZigbeeConnector(config['zigbee']))
    
    # OPC-UA
    if 'opcua' in config:
        for opcua_config in config.get('opcua', []):
            connectors.append(OPCUAConnector(opcua_config))
    
    if not connectors:
        logger.warning("No connectors configured. Please check the configuration file.")
        # Keep running for monitoring
        while True:
            await asyncio.sleep(60)
    
    # Start all connectors
    tasks = [connector.start() for connector in connectors]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
