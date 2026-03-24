from pathlib import Path

from flask import send_from_directory

from api import base as app


@app.route('/', defaults={ 'path': '' })
@app.route('/<path:path>')
def _(path):
	full_path = Path(app.static_folder).joinpath(path)
	if path and full_path.exists():
		is_image = full_path.suffix.endswith(('jpg', 'jpeg', 'png', 'webp'))
		return send_from_directory(app.static_folder, path, as_attachment=not is_image)
	return send_from_directory(app.static_folder, 'index.html')
