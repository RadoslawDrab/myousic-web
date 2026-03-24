from datetime import datetime, timedelta
import json

from utils import Status, get_env
from utils.args import Args
from utils.classes import Singleton
from utils.logger import Logger


class JobManager(Singleton):
	def __init__(self):
		super().__init__()
		self._db_path = Args.output_path.joinpath('db.json')
		self._db = self._get_db()

	@classmethod
	@Singleton.exists
	def _get_db(cls) -> dict:
		self = cls._instance

		if not self._db_path.exists():
			self._set_db({})
		with open(self._db_path, 'r', encoding='utf-8') as fr:
			data: dict[str, dict[str, any]] = json.loads(fr.read())

			filtered_data = {}
			changed = False
			for id, item in data.items():
				available_to = int(item.get('availableTo') or 0)
				if datetime.now().timestamp() * 1000 <= available_to:
					filtered_data[id] = item
					continue

				self._delete_folder(id)
				changed = True

			if changed:
				self._set_db(filtered_data)
			return filtered_data

	@classmethod
	@Singleton.exists
	def _set_db(cls, data: dict | None = None):
		self = cls._instance
		_data = data if data is not None else self._db
		with open(self._db_path, 'w', encoding='utf-8') as f:
			f.write(json.dumps(_data))

	@classmethod
	@Singleton.exists
	def update(cls, job_id: str, status: str, append: bool = True, **kwargs):
		self = cls._instance
		status = status.lower()
		if status not in ['completed', 'pending', 'failed']:
			raise Status(f'Invalid status type "{status}"', 500)
		timestamp = datetime.now().timestamp() * 1000

		if job_id not in self._db:
			self._db[job_id] = {
				'createdAt': timestamp,
				'availableTo': (datetime.now() + timedelta(minutes=max(get_env('SERVER_AUDIO_AVAILABLE', default=48 * 60, type=int), 1))).timestamp() * 1000
			}
			Logger.log(f"Job {job_id} created", log_type='DEBUG')

		self._db[job_id].update({
			'status': status,
			'finished': status != 'pending',
			'updatedAt': timestamp,
			'data': { **self._db[job_id].get('data', {}), **kwargs } if append else kwargs
		})

		self._set_db()

	@classmethod
	@Singleton.exists
	def delete(cls, job_id: str):
		self = cls._instance
		if job_id not in self._db:
			raise Status(404, f'Job f{job_id} not found')
		self._db.pop(job_id)
		self._delete_folder(job_id)
		self._set_db()
		Logger.log(f"Job {job_id} deleted", log_type='DEBUG')
	@classmethod
	@Singleton.exists
	def _delete_folder(cls, job_id: str):
		path = Args.output_path.joinpath(job_id)
		if path.exists():
			for item in path.rglob('*'):
				item.unlink() if item.is_file() else item.rmdir()
			path.rmdir()
	@classmethod
	@Singleton.exists
	def get(cls, job_id: str | None = None):
		self = cls._instance
		self._db = self._get_db()
		if job_id:
			return self._db.get(job_id)

		return [{ 'id': key, **value } for key, value in self._db.items()]