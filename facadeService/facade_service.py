from flask import Response
import requests
import random
import config
from typing import Dict, List
from hazelcastUtils.mq_producer import HazelcastMQProducer

logger = config.logging.getLogger("__name__")

class FacadeService:
    def __init__(self, 
                 logging_urls: List[str], 
                 messages_urls: List[str], 
                 paths: config.ENDPOINT_PATHS, 
                 hazelcast_config=config.HAZELCAST_CLIENT_CONFIG, 
                 hazelcast_mq_name=config.HAZELCAST_MESSAGE_QUEUE_NAME
                 ):
        self.logging_urls = logging_urls
        self.messages_urls = messages_urls
        self.hazelcast_config = hazelcast_config
        self.hazelcast_mq_name = hazelcast_mq_name
        self.paths = paths
        self.post_headers = {"Content-Type": "application/json"}
        self.init_all()
        
    def init_all(self):
        self.set_random_logging_service_url()
        self.set_random_messages_service_url()
        self.producer = HazelcastMQProducer(self.hazelcast_config, self.hazelcast_mq_name)
        
    def set_random_logging_service_url(self):
        self.logging_url = random.choice(self.logging_urls)
        
    def set_random_messages_service_url(self):
        self.messages_url = random.choice(self.messages_urls)
        
    def get_logging_messages(self) -> Response:
        logger.info(f"Getting messages from LoggingService {self.logging_url}{self.paths.logging.get_messages}")
        logging_responce = requests.get(f"{self.logging_url}{self.paths.logging.get_messages}")
        return logging_responce
        
    def get_messages_messages(self) -> Response:
        self.set_random_messages_service_url()
        logger.info(f"Getting messages from MessageService {self.messages_url}{self.paths.messages.get_messages}")
        messages_responce = requests.get(f"{self.messages_url}{self.paths.messages.get_messages}")
        return messages_responce

    def post_message(self, uuid: str, message: str) -> Response:
        self.set_random_logging_service_url()
        self.producer.produce(message)
        return requests.post(url=f"{self.logging_url}{self.paths.logging.post_message}",
                             json={"UUID": uuid, "msg": message}, headers=self.post_headers)

    def get_messages(self) -> Dict[str, str]:
        self.set_random_logging_service_url()
        logging_msg = self.get_logging_messages().text
        messages_msg = self.get_messages_messages().text
        return {"logging_response": logging_msg, "messages_response": messages_msg}
