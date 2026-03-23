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
	JobManager.update(job_id, 'pending', append=False, track=track, url=url)

	download_queue.put({
		'id': job_id,
		'url': url,
		'track': track,
		'args': request.args,
		'host_url': request.host_url + 'api/download/'
		# 'artwork_file': request.files.get('artworkFile')
	})


	raise Status('Download added to queue', 202, **{'job_id': job_id })

@api.route("/download/<path:path>", methods=["GET"])
def download(path: str):
	return send_from_directory(Args.output_path, path, as_attachment=True)