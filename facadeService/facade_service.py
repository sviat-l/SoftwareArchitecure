from flask import Response
import requests
import random
import base
from typing import Dict, List
from hazelcastUtils.mq_producer import HazelcastMQProducer
from hazelcastUtils.abstract_client import discover_hc_config, discover_mq_name
from consulUtils.consul_service import ConsulServiceClient

logger = base.logging.getLogger("__name__")

class FacadeService:
    def __init__(self):
        self.consul_client = ConsulServiceClient()
        self.post_headers = {"Content-Type": "application/json"}
        self.logging_url = None
        self.messages_url = None
        self.init_all()
        
    def init_all(self):
        logger.info("Connecting to HazelcastMQProducer")
        logger.info("Discovering Hazelcast configuration via Consul")
        self.hc_config = discover_hc_config(self.consul_client)
        self.mq_name = discover_mq_name(self.consul_client)
        self.producer = HazelcastMQProducer(self.hc_config, self.mq_name)
        self.set_random_logging_service_url()
        self.set_random_messages_service_url()
        
    def register_service(self):
        logger.info("Registering facade_service with Consul")
        self.consul_client.register_service('facade_service')
        
    def discover_logging_service_urls(self) -> List[str]:
        logger.info("Discovering logging service urls via Consul")
        return self.consul_client.discover_service_addresses("logging_service")
    
    def discover_messages_service_urls(self) -> List[str]:
        logger.info("Discovering messages service urls via Consul")
        return self.consul_client.discover_service_addresses("messages_service")
    
    def set_random_logging_service_url(self):
        self.logging_url = random.choice(self.discover_logging_service_urls())
        
    def set_random_messages_service_url(self):
        self.messages_url = random.choice(self.discover_messages_service_urls())
        
    def get_logging_messages(self) -> Response:
        logger.info(f"Getting messages from LoggingService {self.logging_url}/messages")
        logging_responce = requests.get(f"{self.logging_url}/messages")
        return logging_responce
        
    def get_messages_messages(self) -> Response:
        self.set_random_messages_service_url()
        logger.info(f"Getting messages from MessageService {self.messages_url}/messages")
        messages_responce = requests.get(f"{self.messages_url}/messages")
        return messages_responce

    def post_message(self, uuid: str, message: str) -> Response:
        self.set_random_logging_service_url()
        self.producer.produce(message)
        return requests.post(url=f"{self.logging_url}/message",
                             json={"UUID": uuid, "msg": message}, headers=self.post_headers)

    def get_messages(self) -> Dict[str, str]:
        self.set_random_logging_service_url()
        logging_msg = self.get_logging_messages().text
        messages_msg = self.get_messages_messages().text
        return {"logging_response": logging_msg, "messages_response": messages_msg}
    
    def __del__(self):
        self.producer.shutdown()
        self.consul_client.deregister_service('facade_service')
