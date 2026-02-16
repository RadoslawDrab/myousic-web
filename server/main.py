from flask import Flask, request
from flask_cors import CORS

from api import api, downloads, data
from utils import Status


app = Flask(__name__)
CORS(app)

@app.errorhandler(Status)
def _(error):
	return { 'message': error.message, 'code': error.code, 'timestamp': error.timestamp, **error.kwargs }, error.code

app.route("/api", methods=["GET", "POST"])(api)
app.route("/api/<string:artist>/<string:title>", methods=["GET"])(data)
app.route("/audio/<path:path>", methods=["GET"])(downloads)

def init():
	app.run(port=3001, debug=True)

if __name__ == "__main__":
	init()