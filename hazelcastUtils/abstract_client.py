import hazelcast
import base
from consulUtils.consul_service import ConsulServiceClient

logger = base.logging.getLogger("Abstract-Hazelcast-Client")

def discover_hc_config(consul_client: ConsulServiceClient) -> dict:
    logger.info("Discovering Hazelcast configuration via Consul")
    return {
        "cluster_name": consul_client.get_consul_value("hazelcast/cluster_name"),
        "cluster_members": consul_client.get_consul_value("hazelcast/cluster_members").split("@"),
    }
    
def discover_mq_name(consul_client: ConsulServiceClient) -> str:
    logger.info(f"Discovering Hazelcast message queue name via Consul")
    return consul_client.get_consul_value("hazelcast/mq_name")

class BaseHazelcastClient:
    def __init__(self, hc_config:dict = None):
        self.hc_config = hc_config
        self.consul_client = ConsulServiceClient()
        self.connect()
    
    def connect(self) -> hazelcast.HazelcastClient:
        if self.hc_config is None:
            self.hc_config = self.discover_hc_config()
        logger.info("Connecting to Hazelcast")
        self.client = hazelcast.HazelcastClient(**self.hc_config)
        return self.client
    
    def discover_hc_config(self) -> dict:
        return discover_hc_config(self.consul_client)
        
    def discover_mq_name(self) -> str:
        return discover_mq_name(self.consul_client)
    
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
