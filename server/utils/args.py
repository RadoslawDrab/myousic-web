import argparse
from pathlib import Path

from utils import get_env
from utils.classes import Obj, Singleton

PREVIEW = get_env('PREVIEW', default=False, type=bool)

class Args(Singleton):
	dev: bool = not PREVIEW
	preview: bool = PREVIEW
	output_path: Path = Path('./.preview/audio/' if PREVIEW else get_env('SERVER_OUTPUT_PATH', default='./audio', type=Path))
	temp_path: Path = Path('./tmp')
	log_path: Path = Path('./.preview/file.log' if PREVIEW else './.tmp/file.log')
	port: int = 3001
	host: str = 'localhost'
	app_path: Path = Path.cwd().parent.joinpath('client/dist') if PREVIEW else Path.cwd().joinpath('client')

	def __init__(self) -> None:
		super().__init__()
		parser = argparse.ArgumentParser('myousic-web-server', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

		parser.add_argument('--dev', help='Mark as development', action='store_true', default=self.dev)
		parser.add_argument('--preview', help='Mark as preview', action='store_true', default=self.preview)
		parser.add_argument('--prod', help='Mark as production', action='store_false', dest='dev', default=not self.dev)
		parser.add_argument('--port', '-p', help='Server port', type=int, default=self.port)
		parser.add_argument('--host', help='Server host', type=str, default=self.host)
		parser.add_argument('--output-path', '-o', help='Audio folder', type=Path, default=self.output_path)
		parser.add_argument('--temp-path', help='Audio temporary folder. Relative to `output-path`', type=Path, default=self.temp_path)
		parser.add_argument('--log-path', help='Log file path', type=Path, default=self.log_path)
		parser.add_argument('--app-path', help='Client app folder path', type=Path, default=self.app_path)

		args = parser.parse_args()


		for arg in args.__dict__:
			if arg not in Obj.get_attributes(self.__class__):
				continue
			setattr(self.__class__, arg, getattr(args, arg))