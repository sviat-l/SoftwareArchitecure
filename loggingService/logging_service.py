from hazelcastUtils.abstract_client import BaseHazelcastClient
from hazelcastUtils.abstract_client import discover_hc_config
from consulUtils.consul_service import ConsulServiceClient
import base
import uuid
from typing import List

logger = base.logging.getLogger(__name__)

class LoggingService:
    def __init__(self):
        self.consul_client = ConsulServiceClient()
        logger.info('Starting logging service, checking for Hazelcast client...')
        self.connect_to_hazelcast()
        logger.info(f"Logging service started with created map name: {self.map_name}")
        
    def register_service(self):
        logger.info("Registering logging_service with Consul")
        self.consul_client.register_service('logging_service')
        
    def connect_to_hazelcast(self):
        self.hazelcast_config = discover_hc_config(self.consul_client)
        self.client = BaseHazelcastClient(self.hazelcast_config)
        self.map_name = str(uuid.uuid4())
        self.map = self.client.get_hz_map(self.map_name).blocking()
       
    def get_all_messages(self) -> List[str]:
        return list(self.map.values())

    def post_message(self, uuid, message):
        self.map.put(uuid, message)

    def shutdown(self):
        if self.client:
            self.client.shutdown()
            
    def __del__(self):
        self.shutdown()
