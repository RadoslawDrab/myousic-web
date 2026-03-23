from flask import Blueprint

from utils.args import Args


api = Blueprint("api", __name__)
base = Blueprint("base", __name__, static_folder=Args.app_path)

from . import download, track_data, yt_data, static