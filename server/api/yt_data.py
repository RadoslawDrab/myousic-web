import re
import traceback
import uuid
from datetime import datetime

from flask import request

from . import api
from utils import Status
from utils.args import Args
from utils.logger import Logger
from utils.yt_dlp import get_yt_dlp

@api.route("/yt-data", methods=["GET"])
def yt_data():
	try:
		ydl, file_name = get_yt_dlp(request.args)

		with ydl:
			url = request.args.get('url')

			if not url:
				raise Status('No url provided', 400)

			info = ydl.extract_info(url, download=False)
			title = info.get('title') or info.get('fulltitle')
			artist = info.get('artist') or info.get('uploader')

			extracted_title = re.sub(r'\(official.+video\)', '', title, flags=re.IGNORECASE)
			extracted_title = re.sub(f'{artist.lower()} *- *', '', extracted_title, flags=re.IGNORECASE)
			extracted_title = extracted_title.strip()

			upload_date = re.search(r'(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})', info.get('upload_date', ''))
			upload_date = upload_date.groupdict() if upload_date else {}

			upload_date_timestamp = datetime(int(upload_date.get('year', 0)), int(upload_date.get('month', 0)), int(upload_date.get('day', 0))).timestamp()

			duration = info.get('duration_string')

			duration_match = re.match(r'(?P<hours>\d*?):?(?P<minutes>\d*?):?(?P<seconds>\d+?)$', str(duration)) if duration else None
			if duration_match:
				duration_times = duration_match.groupdict()
				duration = 0
				duration += int(duration_times.get('hours', 0) or 0) * 60 * 60 * 1000
				duration += int(duration_times.get('minutes', 0) or 0) * 60 * 1000
				duration += int(duration_times.get('seconds', 0) or 0) * 1000

			Logger.log(f'Audio data retrieved [{artist} - {extracted_title}]', log_type='DEBUG', print_only=Args.dev)

			return {
				'id': uuid.uuid4(),
				'fullTitle': title,
				'title': extracted_title,
				'artist': artist,
				'url': url,
				'artworkUrl': info.get('thumbnail'),
				'trackTimeMillis': 0 if type(duration) == str else duration,
				'releaseData': round(upload_date_timestamp * 1000, 0),
			}
	except Exception as e:
		Logger.log(traceback.format_exc(), log_type='ERROR')
		raise Status(str(e), 500)