from typing import Dict, Any
from hazelcastUtils.abstract_client import BaseHazelcastClient
import config

logger = config.logging.getLogger("Hazelcast-MQ-Producer")
                     
class HazelcastMQProducer(BaseHazelcastClient):
    def __init__(self, hc_config: Dict[str, Any], map_name: str):
        super().__init__(hc_config)
        self.map_name = map_name
        self.mq = self.get_hz_queue(self.map_name)
        
    def produce(self, message: str):
        try:
            self.mq.put(message)
            logger.info(f"Produced message: {message}")
        except Exception as e:
            logger.error(f"Error producing message: {e}")
