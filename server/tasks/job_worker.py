import queue
import traceback
from pathlib import Path

from tasks.job_manager import JobManager
from utils.args import Args
from utils.logger import Logger
from utils.track import get_track
from utils.yt_dlp import get_yt_dlp


download_queue = queue.Queue()

JobManager()


def job_worker(**kwargs):
	data: dict | None = download_queue.get()
	if data is None:
		return
	job_id = data['id']
	args = data.get('args', {})
	url = data.get('url', '')
	track = data.get('track', {})
	artwork_size = int(args.get('artworkSize', 1000))

	JobManager.update(job_id, 'pending')

	try:
		ydl, file_name = get_yt_dlp(data.get('args'), job_id)
		download_folder = Args.output_path.joinpath(job_id)
		download_folder.mkdir(exist_ok=True)
		with ydl:
			audio, target_file_path, artwork_file_path = get_track(
				ydl,
				url,
				download_folder.joinpath(file_name),
				track,
				artwork_size=artwork_size
			)
			audio.save()

			Logger.log(f'Audio "{target_file_path.name}" saved to "{Path.cwd().joinpath(target_file_path.parent).as_posix()}"', log_type='DEBUG')
			JobManager.update(
				job_id,
				'completed',
				fileName=target_file_path.name,
				downloadUrl=data.get('host_url', '/') + target_file_path.relative_to(Args.output_path).as_posix(),
				artworkUrl=data.get('host_url', '/') + artwork_file_path.relative_to(Args.output_path).as_posix()
			)
	except Exception as e:
		JobManager.update(job_id, 'failed', error=str(e))
		Logger.log(traceback.format_exc(), log_type='ERROR')
	finally:
		download_queue.task_done()