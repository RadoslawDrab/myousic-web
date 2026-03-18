import sys
from pathlib import Path

from flask import Flask, send_from_directory
from flask_cors import CORS
from waitress import serve

import tasks
from api import api, downloads, data
from utils import Status
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

@app.route('/', defaults={ 'path': '' })
@app.route('/<path:path>')
def _(path):
	full_path = Path(app.static_folder).joinpath(path)
	if path and full_path.exists():
		return send_from_directory(app.static_folder, path, as_attachment=True)
	return send_from_directory(app.static_folder, 'index.html')

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

	Logger.log(f'MODE: { "development" if Args.dev and not Args.preview else ("preview" if Args.preview else "production") }', log_type='DEBUG')

	if not Args.dev or Args.preview:
		Logger.log(f'Server started on http://{Args.host}:{Args.port}', log_type='INFO')

		serve(
			app,
			host=Args.host,
			port=Args.port,
			threads=12,
			connection_limit=200,
			channel_timeout=60
        )
	else:
		app.run(
			port=Args.port,
			debug=True,
			host=Args.host
		)

if __name__ == "__main__":
	init()