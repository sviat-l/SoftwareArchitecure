import consul
import os
import utils
import socket
from typing import List

logger = utils.logging.getLogger(__name__)

class ConsulServiceClient:
    def __init__(self, port=None, host=None):
        self.port = port
        self.host = host
        self.client = self.get_consul_client()

    def get_consul_client(self):
        self.host = os.getenv("CONSUL_HOST", "localhost") if self.host is None else self.host
        self.port = int(os.getenv("CONSUL_PORT", "8500")) if self.port is None else self.port
        return consul.Consul(host=self.host, port=self.port, scheme="http")
    
    def get_consul_value(self, key: str) -> str:
        _, data = self.client.kv.get(key)
        value =  data["Value"].decode("utf-8") if data else None
        logger.info(f"Consul extracted for key {key} value: {value}")
        return value
    
    def discover_service_addresses(self, service_name: str) -> List[str]:
        extracted_urls = []
        _, services = self.client.health.service(service_name, passing=True)
        for entry in services:
            if "Service" not in entry:
                continue
            host = entry["Service"]["Address"]
            port = entry["Service"]["Port"]
            extracted_urls.append(f"http://{host}:{port}")
        extracted_urls = list(set(extracted_urls))
        logger.info(f"Consul extracted for service {service_name} urls: {extracted_urls}")
        return extracted_urls

    def get_service_info(self, service_name: str) -> str:
        service_host = socket.gethostname()
        service_port = int(os.environ["PORT"])
        return [service_name, service_host, service_port]
    
    def get_service_id(self, name: str, host: str, port: int) -> str:
        return f"{name}@{host}@{port}"
    
    def register_service(self, service_name: str) -> None:
        name, host, port = self.get_service_info(service_name)
        service_id = self.get_service_id(name, host, port)
        host = socket.gethostbyname(host)
        logger.info(f"Registering service: {service_id}, with address: {host}:{port}")
        self.client.agent.service.register(
            name=name,
            service_id=service_id,
            address=host,
            port=port,
            check={"http": f"http://{host}:{port}/health", 
                   "interval": "10s", 
                   "timeout": "1s"
                   }
        )
        
    def deregister_service(self, service_name: str):
        service_id = self.get_service_id(*self.get_service_info(service_name))
        print(f"Deregistering service: {service_id}")
        self.client.agent.service.deregister(service_id)
