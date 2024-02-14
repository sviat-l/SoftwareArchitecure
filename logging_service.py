from flask import Flask, request

app = Flask(__name__)
DB = {}


@app.route('/get_all_messages', methods=['GET'])
def get_messages():
    messages = list(DB.values())
    print(f"Successful GET method to logging service, returning all {len(messages)} messages")
    return '\n|'.join(messages)


@app.route('/post_message', methods=['POST'])
def post_message():
    uuid = request.json['UUID']
    message = request.json['msg']
    DB[uuid] = message
    print("Posted message:", message, "from user:", uuid)
    return {"status": "success"}
    

if __name__ == '__main__':
    app.run(port=4201)
