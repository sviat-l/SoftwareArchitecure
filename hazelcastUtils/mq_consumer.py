from hazelcastUtils.abstract_client import BaseHazelcastClient
from threading import Thread, Lock
from typing import List
import utils

logger = utils.logging.getLogger("Hazelcast-MQ-Consumer")        
        
class HazelcastMQConsumer(BaseHazelcastClient):
    def __init__(self, hc_config=None, mq_name=None):
        super().__init__(hc_config)
        self.messages = []
        self.lock = Lock()
        self.thread = None
        self.mq_name = mq_name
        self.mq = self.get_hz_queue(self.mq_name)
        
    def consume(self):       
        while True:
            try:
                with self.lock:
                    message = self.mq.take()
                logger.info(f"Consumed message: {message}")
                self.messages.append(message)
            except Exception as e:
                logger.error(f"Error consuming message: {e}")
    
    def start_consumer(self):
        logger.info("Starting consumer thread")
        self.thread = Thread(target=self.consume, daemon=True)
        self.thread.start()
        
    def get_consumed_messages(self) -> List[str]:    
        logger.info("Returning consumed messages from HazelcastMQ")
        return self.messages
    
    def __del__(self):
        super().__del__()
        self.thread.join()    
