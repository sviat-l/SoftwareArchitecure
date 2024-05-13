from typing import List
import config
from hazelcastUtils.mq_consumer import HazelcastMQConsumer

logger = config.logging.getLogger(__name__)

class MessagesService:
    def __init__(self, 
                 hazelcast_config: dict=config.HAZELCAST_CLIENT_CONFIG, 
                 hazelcast_mq_name: str=config.HAZELCAST_MESSAGE_QUEUE_NAME
                 ):
        self.hazelcast_config = hazelcast_config
        self.hazelcast_mq_name = hazelcast_mq_name
        self.connect_to_hazelcast()
        
    def connect_to_hazelcast(self):
        self.consumer = HazelcastMQConsumer(self.hazelcast_config, self.hazelcast_mq_name)
        self.consumer.start_consumer()
        
    def get_messages(self) -> List[str]:
        logger.info("Trying to get messages from HazelcastMQConsumer")
        return self.consumer.get_consumed_messages()

    def close(self):
        self.consumer.close
        
    def __deler__(self):
        self.close()