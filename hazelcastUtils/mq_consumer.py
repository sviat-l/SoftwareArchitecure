from typing import Dict, Any, List
from threading import Thread, Lock
from hazelcastUtils.abstract_client import BaseHazelcastClient
import config

logger = config.logging.getLogger("Hazelcast-MQ-Consumer")        
        
class HazelcastMQConsumer(BaseHazelcastClient):
    def __init__(self, hc_config: Dict[str, Any], queue_name: str):
        super().__init__(hc_config)
        self.queue_name = queue_name
        self.messages = []
        self.lock = Lock()
        self.mq = self.get_hz_queue(self.queue_name)
        self.thread = None
        
    def consume(self, messages: List[str]):       
        while True:
            try:
                with self.lock:
                    message = self.mq.take()
                logger.info(f"Consumed message: {message}")
                messages.append(message)
            except Exception as e:
                logger.error(f"Error consuming message: {e}")
    
    def start_consumer(self):
        logger.info("Starting consumer thread")
        storage = self.messages
        self.thread = Thread(target=self.consume, args=(storage,), daemon=True)
        self.thread.start()
        
    def get_consumed_messages(self) -> List[str]:    
        logger.info("Returning consumed messages from HazelcastMQ")
        return self.messages
    
    def close(self):
        super().close()
        self.thread.join()    
