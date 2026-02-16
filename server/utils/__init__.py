from datetime import datetime

from flask import Request


class Status(Exception):
	def __init__(self, message, code, **kwargs):
		self.message = message
		self.code = code
		self.timestamp = datetime.now().timestamp() * 1000
		self.kwargs = kwargs

def find_lyrics_provider(self):
	i = 0
	while not self.valid_lyrics() and len(self._lyrics) > 1 and i <= len(self._lyrics_providers):
		self._lyrics.pop(0)
		i += 1

def get_args(request: Request, arg: str, filter_empty: bool = True):
	return [v for v in (request.args.get(arg, '').split(',') if request.args.get(arg) else []) if (v if filter_empty else True)]