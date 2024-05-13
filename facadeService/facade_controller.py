from flask import Flask, request, Response, jsonify
from facade_service import FacadeService
from uuid import uuid4
import argparse
import config

logger = config.logging.getLogger(__name__)
app = Flask(__name__)

logging_service_urls = config.get_logging_service_urls() 
message_service_urls = config.get_message_service_urls()
# logging_service_urls, message_service_urls = config.LOGGING_SERVICE_URLS, config.MESSAGE_SERVICE_URLS
endpoint_paths = config.ENDPOINT_PATHS
facade_service = FacadeService(logging_service_urls, message_service_urls, endpoint_paths)

@app.route('/messages', methods=['GET'])
def get_messages() -> Response:
    try: 
        logger.info("Getting messages from services")
        messages = facade_service.get_messages()
        logging_response = messages['logging_response']
        messages_response = messages['messages_response']
    except Exception as e:
        logger.error(f"Failed to get messages. Error occured: {e}")
        return Response(status=500, response=f"Failed to get messages:\n{e}")
    logger.info(f"Messages-Service received messages: {messages_response}")
    logger.info(f"Logging-Serice received messages: {logging_response}")
    result = {"logging": logging_response, "messages": messages_response}
    return jsonify(result)


@app.route('/message', methods=['POST'])
def send_message() -> Response:
    msg_uuid = str(uuid4())
    try:
        msg = request.json['msg']
    except Exception as e:
        logger.error(f"Failed to process the request. Error occured:\n{e}")
        return Response(status=400, response=f"Failed to preprocess message, error occured:\n{e}")

    response = facade_service.post_message(msg_uuid, msg)
    if response.status_code == 200:
        logger.info(f"Posted message: {msg} from user: {msg_uuid}")
        return Response(status=200, response="Message posted successfully")
    
    if response.status_code == 400:
        logger.error(f"Bad Request: {response.text}")
        return Response(status=400, response=f"Bad Request: {response.text}")
    if response.status_code == 500:
        logger.error(f"Server Error: {response.text}")
        return Response(status=500, response=f"Server Error: {response.text}")
    logger.error(f"Unexpected response: {response.status_code}, {response.text}")
    return Response(status=500, response=f"Unexpected response: {response.status_code}, {response.text}")

@app.route('/', methods=['GET'])
def home() -> Response:
    return Response(status=200, response="Welcome to the facade service")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int,
                        default=config.FACADE_SERVICE_PORT, help="Port number for the app service")
    parser.add_argument("--debug", action="store_true",
                        help="Enable debug mode for the service app")
    args = parser.parse_args()
    app.run(port=args.port, debug=args.debug)
