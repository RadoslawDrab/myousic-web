import os
from datetime import datetime
from typing import TypeVar, overload

from flask import Request


class Status(Exception):
	def __init__(self, message, code, **kwargs):
		self.message = message
		self.code = code
		self.timestamp = datetime.now().timestamp() * 1000
		self.kwargs = kwargs

ENV_T = TypeVar('ENV_T')

@overload
def get_env() -> dict[str, str]: ...
@overload
def get_env(key: str, default: ENV_T = None, type: any = str) -> ENV_T | None: ...
@overload
def get_env(*key: str, default: ENV_T = None, type: any = str) -> list[ENV_T]: ...
def get_env(*key: str, default: ENV_T = None, type: any = str) -> dict[str, str] | list[ENV_T] | ENV_T | None:
	"""
	A flexible utility to retrieve one or more environment variables.

	- No arguments: Returns a dictionary of all environment variables.
	- One argument: Returns the value of a single environment variable.
	- Multiple arguments: Returns a list of values for the specified variables.

	Args:
	    *key: The name(s) of the environment variable(s) to retrieve.
	    default: The default value to return if a variable is not found.
	    type: The type of the environment variable(s) to retrieve.

	Returns:
	    A dictionary, a single string, a list of strings, or None.
	"""
	# If no keys are provided, return all environment variables as a dictionary.
	if len(key) == 0:
		return dict(os.environ) or default
	# If one key is provided, return its value.
	if len(key) == 1:
		return type(os.getenv(key[0], default))
	# If multiple keys are provided, return a list of their values.
	else:
		return [type(os.getenv(key, default)) for key in key]

def get_args(request: Request, arg: str, filter_empty: bool = True):
	return [v for v in (request.args.get(arg, '').split(',') if request.args.get(arg) else []) if (v if filter_empty else True)]