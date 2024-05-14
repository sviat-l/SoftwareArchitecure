from messages_service import MessagesService
from flask import Flask, Response
import argparse
import base

logger = base.logging.getLogger(__name__)

app = Flask(__name__)

messages_service = MessagesService()

@app.route('/messages', methods=['GET'])
def get_messages() -> Response:
    try:
        logger.info("Getting messages from MessageService")
        result = messages_service.get_messages()
        result = "|".join(result)
    except Exception as e:
        logger.error(f"Failed to GET request for MessageService, error occured: {e}")
        return Response(status=500, response=f"Failed to get messages from MessageService:\n{e}")
    logger.info("Successful GET request for MessageService")
    return Response(status=200, response=result)

@app.route('/', methods=['GET'])
@app.route('/health', methods=['GET'])
def home() -> Response:
    return Response(status=200, response="Welcome to the message service")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, help="Port number for the app service")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode for the service app")
    args = parser.parse_args()
    
    import threading
    import time
    def thread_register_service():
        time.sleep(0.1)
        messages_service.register_service()
    t1 = threading.Thread(target=thread_register_service, daemon=True)
    t1.start()
    
    app.run(port=args.port, debug=args.debug)
