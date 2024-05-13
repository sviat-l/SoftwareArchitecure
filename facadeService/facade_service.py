from flask import Response
import requests
import random
import config
from typing import Dict, List

logger = config.logging.getLogger("__name__")

class FacadeService:
    def __init__(self, 
                 logging_urls: List[str], 
                 messages_url: str, 
                 paths: config.ENDPOINT_PATHS, 
                 ):
        self.logging_urls = logging_urls
        self.messages_url = messages_url
        self.logging_url = None
        self.paths = paths
        self.post_headers = {"Content-Type": "application/json"}
        
    def set_random_logging_service_url(self):
        self.logging_url = random.choice(self.logging_urls)
        
    def get_logging_messages(self) -> Response:
        logger.info(f"Getting messages from LoggingService {self.logging_url}{self.paths.logging.get_messages}")
        logging_responce = requests.get(f"{self.logging_url}{self.paths.logging.get_messages}")
        return logging_responce
        
    def get_messages_message(self) -> Response:
        logger.info(f"Getting message from MessagesService {self.messages_url}{self.paths.messages.get_static_message}")
        return requests.get(f"{self.messages_url}{self.paths.messages.get_static_message}")

    def post_message(self, uuid: str, message: str) -> Response:
        self.set_random_logging_service_url()
        return requests.post(url=f"{self.logging_url}{self.paths.logging.post_message}",
                             json={"UUID": uuid, "msg": message}, headers=self.post_headers)

    def get_messages(self) -> Dict[str, str]:
        self.set_random_logging_service_url()
        logging_msg = self.get_logging_messages().text
        messages_msg = self.get_messages_message().text
        return {"logging_response": logging_msg, "messages_response": messages_msg}
