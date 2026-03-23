from flask import Flask
from flask_cors import CORS
from waitress import serve

import tasks
from api import api, base
from utils import Status
from utils.logger import Logger, LoggerFormat
from utils.tasks import TasksHandler
from utils.args import Args

Args()

Args.output_path.mkdir(exist_ok=True, parents=True)

app = Flask(__name__, static_folder=Args.app_path)

CORS(app, origins=["*" if Args.dev else f"http://{Args.host}:{Args.port}"])


@app.errorhandler(Status)
def _(error):
	return { 'message': error.message, 'code': error.code, 'timestamp': error.timestamp, **error.kwargs }, error.code

app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(base, url_prefix="/")

# Configure logging
Logger(
	Args.log_path,
	default_log_type='DEBUG',
	error_log_type='ERROR',
	logger_format=LoggerFormat(show_traceback=True),
	print_only=Args.dev,
	min_log_level=Args.log_level
)

def init():
	TasksHandler.set_kwargs(app=app)
	TasksHandler.start()

	Logger.log(f'MODE: { "development" if Args.dev and not Args.preview else ("preview" if Args.preview else "production") }', log_type='DEBUG')
	Logger.log(f'Min log type "{Args.log_level}"', log_type='DEBUG', print_message=True)

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