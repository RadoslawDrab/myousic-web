import argparse
from pathlib import Path

from utils import get_env
from utils.classes import Obj, Singleton

PREVIEW = get_env('PREVIEW', default=False, type=bool)

class Args(Singleton):
	dev: bool = not PREVIEW
	preview: bool = PREVIEW
	output_path: Path = get_env('SERVER_OUTPUT_PATH', default='./.preview/audio/' if PREVIEW else './audio', type=Path)
	log_path: Path = get_env('SERVER_LOG_PATH', default='./.preview/file.log' if PREVIEW else './.tmp/file.log', type=Path)
	log_level: str = get_env('SERVER_LOG_LEVEL', default='INFO' if PREVIEW else 'DEBUG')
	port: int = 3001
	host: str = 'localhost'
	app_path: Path = Path.cwd().parent.joinpath('client/dist') if PREVIEW else Path.cwd().joinpath('client')
	job_workers: int = 3

	def __init__(self) -> None:
		super().__init__()
		parser = argparse.ArgumentParser('myousic-web-server', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

		parser.add_argument('--dev', help='Mark as development', action='store_true', default=self.dev)
		parser.add_argument('--preview', help='Mark as preview', action='store_true', default=self.preview)
		parser.add_argument('--prod', help='Mark as production', action='store_false', dest='dev', default=not self.dev)
		parser.add_argument('--port', '-p', help='Server port', type=int, default=self.port)
		parser.add_argument('--host', help='Server host', type=str, default=self.host)
		parser.add_argument('--output-path', '-o', help='Audio download folder', type=Path, default=self.output_path)
		parser.add_argument('--log-path', help='Log file path', type=Path, default=self.log_path)
		parser.add_argument('--log-level', help='Log level. Available [\'DEBUG\', \'INFO\', \'WARNING\', \'ERROR\']', default=self.log_level, choices=['DEBUG', 'INFO',' WARNING', 'ERROR'])
		parser.add_argument('--app-path', help='Client app folder path', type=Path, default=self.app_path)
		parser.add_argument('--job-workers', '-w', help='How many workers should download asynchronously. More workers = faster downloads', type=int, default=self.job_workers)

		args = parser.parse_args()


		for arg in args.__dict__:
			if arg not in Obj.get_attributes(self.__class__):
				continue
			setattr(self.__class__, arg, getattr(args, arg))