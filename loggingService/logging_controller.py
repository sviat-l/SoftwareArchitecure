from logging_service import LoggingService
from flask import Flask, request, Response
import argparse
import utils

logger = utils.logging.getLogger(__name__)

app = Flask(__name__)

logging_service = LoggingService()

@app.route('/messages', methods=['GET'])
def get_messages() -> Response:
    try:
        messages = logging_service.get_all_messages()
    except Exception as e:
        logger.error(f"Failed to get all messages, error occured: {e}")
        return Response(status=500, response=f"Failed to get all messages:\n{e}")
    messages_str = '|'.join(messages)
    logger.info(f"Successful GET method to logging service, returning all {len(messages)} messages")
    return Response(status=200, response=messages_str)

@app.route('/message', methods=['POST'])
def post_message() -> Response:
    try:
        uuid, message = request.json['UUID'], request.json['msg']
    except Exception as e:
        logger.error(f"Failed to process the request. Error occured: {e}, ")
        return Response(status=400, response=f"Failed to post message, error occured:\n{e}")
    try:
        logging_service.post_message(uuid, message)
        logger.info(f"Posted message: {message} from user: {uuid}")
    except Exception as e:
        logger.error(f"Failed to post message, error occured: {message} from user: {uuid}")
        return Response(status=500, response=f"Failed to post message, error occured:\n{e})")
    return Response(status=200, response="Message successfully posted")

@app.route('/shutdown', methods=['POST'])
def shutdown() -> Response:
    logger.info("Shutting down logging service")
    try:
        logging_service.shutdown()
    except Exception as e:
        logger.error(f"Failed to shut down logging service, error occured: {e}")
        return Response(status=500, response=f"Failed to shut down logging service:\n{e}")
    return Response(status=200, response="Logging service successfully shut down")

@app.route('/', methods=['GET'])
@app.route('/health', methods=['GET'])
def home() -> Response:
    return Response(status=200, response="Welcome to the logging service")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, help="Port number for the app service")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode for the service app")
    parser.add_argument("--host", type=str, help="Host address for the app service")
    parser.set_defaults(host=utils.get_current_host())
    args = parser.parse_args()
    
    logging_service.register_service()
    app.run(host=args.host, port=args.port, debug=args.debug)
