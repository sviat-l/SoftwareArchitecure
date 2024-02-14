from flask import Flask, request
from uuid import uuid4
import requests

app = Flask(__name__)
logging_service_url = "http://localhost:4201"
message_service_url = "http://localhost:4202"


@app.route('/get_messages', methods=['GET'])
def get_messages():
    logging_msg = requests.get(f"{logging_service_url}/get_all_messages").text
    messages_msg = requests.get(f"{message_service_url}/get_static_msg").text
    print(f"Successful GET request for Facade Service: logging messages with length \
    				- {len(logging_msg)} and from messages - {len(messages_msg)}")
    return {"logging_responce":logging_msg, "messages_responce":messages_msg}


@app.route('/send', methods=['POST'])
def send_message():
	msg_uuid = str(uuid4())
	msg = request.json['msg']
	requests.post(f"{logging_service_url}/post_message", json={"UUID": msg_uuid, "msg": msg})
	print("Message with uuid {msg_uuid} sucсessfully sent")
	return {"status":"success"}
    

if __name__ == '__main__':
    app.run(port=4200)
