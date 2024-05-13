from messages_service import MessagesService
from flask import Flask, Response
import argparse
import config

logger = config.logging.getLogger(__name__)

app = Flask(__name__)

messages_service = MessagesService()

@app.route('/message', methods=['GET'])
def get_static_message() -> Response:
    try:
        result = messages_service.get_static_message()
    except Exception as e:
        logger.error(f"Failed to GET request for MessageService, error occured: {e}")
        return Response(status=500, response=f"Failed to get message from MessageService:\n{e}")
    logger.info("Successful GET request for MessageService")
    return Response(status=200, response=result)

@app.route('/', methods=['GET'])
def home() -> Response:
    return Response(status=200, response="Welcome to the message service")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=config.MESSAGES_SERVICE_PORT, help="Port number for the app service")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode for the service app")
    args = parser.parse_args()
    app.run(port=args.port, debug=args.debug)
