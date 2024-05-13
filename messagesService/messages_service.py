import config

logger = config.logging.getLogger(__name__)

class MessagesService:        
    def get_static_message(self) -> str:
        logger.info("Getting static message")
        return "not implemented yet"
