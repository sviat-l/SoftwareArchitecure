import hazelcast

from config import logging

logger = logging.getLogger("Base-Hazelcast-Client")

class BaseHazelcastClient:
    def __init__(self, hc_config: dict):
        self.hc_config = hc_config
        self.connect()
    
    def connect(self) -> hazelcast.HazelcastClient:
        logger.info("Connecting to Hazelcast")
        self.client = hazelcast.HazelcastClient(**self.hc_config)
        return self.client
    
    def shutdown(self):
        if self.client:
            logger.info("Shutting down Hazelcast")
            self.client.shutdown()
            
    def __del__(self):
        self.shutdown()
        
    def get_hz_map(self, map_name: str):
        logger.info(f"Getting Hazelcast map: {map_name}")
        return self.client.get_map(map_name).blocking()
    
    def get_hz_queue(self, queue_name: str):
        logger.info(f"Getting Hazelcast queue: {queue_name}")
        return self.client.get_queue(queue_name).blocking()
