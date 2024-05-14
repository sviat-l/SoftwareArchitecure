from messages_service import MessagesService
from flask import Flask, Response
import argparse
import utils

logger = utils.logging.getLogger(__name__)

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
    print("current host is: ", utils.get_current_host())
    return Response(status=200, response="Welcome to the message service")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, help="Port number for the app service")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode for the service app")
    parser.add_argument("--host", type=str, help="Host address for the app service")
    parser.set_defaults(host=utils.get_current_host())
    args = parser.parse_args()
    
    messages_service.register_service()
    app.run(host=args.host, port=args.port, debug=args.debug)
