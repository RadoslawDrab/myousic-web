from pathlib import Path

from flask import abort, send_from_directory

from api import base as app
from utils.logger import Logger


@app.route('/', defaults={ 'path': '' })
@app.route('/<path:path>')
def _(path: str):
	if path.startswith('api'):
		return abort(404)
	if path:
		Logger.log(f'Requested "{path}" from "{app.static_folder}"', log_type='DEBUG')

	full_path = Path(app.static_folder).joinpath(path)
	if path and full_path.exists():
		return send_from_directory(app.static_folder, path, as_attachment=False)
	return send_from_directory(app.static_folder, 'index.html', as_attachment=False)
