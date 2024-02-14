from flask import Flask

app = Flask(__name__)


@app.route('/get_static_msg', methods=['GET'])
def get_static_message():
    print("Successful GET request for static method")
    return 'not implemented yet'


if __name__ == '__main__':
    app.run(port=4202)
