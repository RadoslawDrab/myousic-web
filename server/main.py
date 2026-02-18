from pathlib import Path

from flask import Flask
from flask_cors import CORS

from api import api, downloads, data
from utils import Status, get_env
from utils.logger import Logger, LoggerFormat
from utils.tasks import TasksHandler

output_path = Path(get_env('OUTPUT_PATH', default='./audio'))
temp_path = Path(get_env('TEMP_PATH', default='./temp'))
output_path.mkdir(exist_ok=True)

app = Flask(__name__)
CORS(app)

@app.errorhandler(Status)
def _(error):
	return { 'message': error.message, 'code': error.code, 'timestamp': error.timestamp, **error.kwargs }, error.code

app.route("/api", methods=["GET", "POST"])(api)
app.route("/api/<string:artist>/<string:title>", methods=["GET"])(data)
app.route("/audio/<path:path>", methods=["GET"])(downloads)

# Configure logging
Logger(
	'./data/file.log',
	default_log_type='DEBUG',
	error_log_type='ERROR',
	logger_format=LoggerFormat(show_traceback=True)
)

def init():
	import tasks
	TasksHandler.set_kwargs(app=app, output_path=output_path, temp_path=temp_path)
	TasksHandler.start()
	app.run(port=3001, debug=True)

if __name__ == "__main__":
	init()