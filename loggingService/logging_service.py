from hazelcast import HazelcastClient
import config
import uuid
from typing import List

logger = config.logging.getLogger(__name__)

class LoggingService:
    def __init__(self, hazelcast_config=config.HAZELCAST_CLIENT_CONFIG):
        self.hazelcast_config = hazelcast_config
        logger.info('Starting logging service, checking for Hazelcast client...')
        self.connect_to_hazelcast()
        logger.info(f"Logging service started with map name: {self.map_name}")
        
    def connect_to_hazelcast(self):
        self.client = HazelcastClient(**self.hazelcast_config)
        self.map_name = str(uuid.uuid4())
        self.map = self.client.get_map(self.map_name).blocking()
       
    def get_all_messages(self) -> List[str]:
        return list(self.map.values())

    def post_message(self, uuid, message):
        self.map.put(uuid, message)

    def shutdown(self):
        if self.client:
            self.client.shutdown()
            
    def __del__(self):
        self.shutdown()
