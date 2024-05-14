from hazelcastUtils.abstract_client import BaseHazelcastClient
import base

logger = base.logging.getLogger("Hazelcast-MQ-Producer")
                     
class HazelcastMQProducer(BaseHazelcastClient):
    def __init__(self, hc_config=None, mq_name=None):
        super().__init__(hc_config)
        self.mq_name = mq_name if mq_name is not None else self.discover_mq_name()
        self.mq = self.get_hz_queue(self.mq_name)
        
    def produce(self, message: str):
        try:
            self.mq.put(message)
            logger.info(f"Produced message: {message}")
        except Exception as e:
            logger.error(f"Error producing message: {e}")
