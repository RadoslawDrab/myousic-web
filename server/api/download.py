import json
import uuid

from flask import request, send_from_directory

from tasks.job_manager import JobManager
from . import api
from utils import Status
from utils.args import Args
from tasks.job_worker import download_queue

@api.route('/status', methods=["GET"])
def status():
	job_id = request.args.get('id')
	return JobManager.get(job_id)

@api.route("/queue", methods=["POST"])
def queue():
	body: dict[str, any] = json.loads(request.form.get('body', '{}'))

	url: str = body.get('url')
	track: dict = body.get('track')

	if url is None or track is None:
		raise Status('No url or track provided', 400)

	job_id = str(uuid.uuid4())
	host_url = request.host_url + 'api/download/'
	output_folder = Args.output_path.joinpath(job_id)
	output_folder.mkdir(exist_ok=True)
	artwork_file_path = output_folder.joinpath(f'artwork.jpeg')

	artwork_file = request.files.get('artworkFile')
	if artwork_file:
		artwork_file.save(artwork_file_path)

		track = track | { 'artworkUrl100': host_url + artwork_file_path.relative_to(Args.output_path).as_posix() }

	JobManager.update(job_id, 'pending', append=False, track=track, url=url)


	download_queue.put({
		'id': job_id,
		'url': url,
		'track': track,
		'args': request.args,
		'host_url': host_url
	})


	raise Status('Download added to queue', 202, **{'job_id': job_id })

@api.route("/download/<path:path>", methods=["GET"])
def download(path: str):
	return send_from_directory(Args.output_path, path, as_attachment=True)