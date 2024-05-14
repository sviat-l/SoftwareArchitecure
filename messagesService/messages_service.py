from typing import List
import base
from hazelcastUtils.mq_consumer import HazelcastMQConsumer
from consulUtils.consul_service import ConsulServiceClient
from hazelcastUtils.abstract_client import discover_mq_name, discover_hc_config


logger = base.logging.getLogger(__name__)

class MessagesService:
    def __init__(self):
        self.consul_client = ConsulServiceClient()
        self.connect_to_hazelcast()
        
    def register_service(self):
        self.consul_client.register_service('messages_service')
        
    def connect_to_hazelcast(self):
        logger.info("Connecting to HazelcastMQConsumer")
        logger.info("Discovering Hazelcast configuration via Consul")
        self.hc_config = discover_hc_config(self.consul_client)
        self.mq_name = discover_mq_name(self.consul_client)
        self.consumer = HazelcastMQConsumer(self.hc_config, self.mq_name)
        self.consumer.start_consumer()
        
    def get_messages(self) -> List[str]:
        logger.info("Trying to get messages from HazelcastMQConsumer")
        return self.consumer.get_consumed_messages()

    def close(self):
        self.consumer.close
        
    def __deler__(self):
        self.close()
