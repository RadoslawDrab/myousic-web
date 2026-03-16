from pathlib import Path

from flask import Flask
from flask_cors import CORS

from api import api, downloads, data
from utils import Status, get_env
from utils.logger import Logger, LoggerFormat
from utils.tasks import TasksHandler
from utils.args import Args

Args()

Args.output_path.mkdir(exist_ok=True, parents=True)

app = Flask(__name__, static_folder=Args.app_path)
CORS(app)

@app.errorhandler(Status)
def _(error):
	return { 'message': error.message, 'code': error.code, 'timestamp': error.timestamp, **error.kwargs }, error.code

app.route("/api", methods=["GET", "POST"])(api)
app.route("/api/<string:artist>/<string:title>", methods=["GET"])(data)
app.route("/audio/<path:path>", methods=["GET"])(downloads)

# Configure logging
Logger(
	Args.log_path,
	default_log_type='DEBUG',
	error_log_type='ERROR',
	logger_format=LoggerFormat(show_traceback=True)
)

def init():
	TasksHandler.set_kwargs(app=app, output_path=Args.output_path, temp_path=Args.temp_path)
	TasksHandler.start()
	app.run(port=3001, debug=True)

if __name__ == "__main__":
	init()