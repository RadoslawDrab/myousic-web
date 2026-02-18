import traceback
from datetime import datetime
import re
import uuid
from pathlib import Path

from flask import request, send_from_directory

from providers import find_lyrics_provider
from utils import Status, get_args, get_env
from yt_dlp import YoutubeDL

from utils.logger import Logger
from utils.track import get_track
from utils.track_data import Genre, Lyrics

output_path = Path(get_env('OUTPUT_PATH', default='./audio'))
temp_path = Path(get_env('TEMP_PATH', default='./temp'))

def api():
	try:
		id = uuid.uuid4()
		file_name = f'{id}.m4a'
		ydl = YoutubeDL({
			'format': 'm4a/bestaudio/best',
			'outtmpl': file_name,
			'quiet': True,
			'postprocessors': [{  # Extract audio using ffmpeg
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'm4a',
			}],
			'paths': {
				'home': str(output_path),
				'temp': str(temp_path)
			}
		})

		with ydl:
			# POST
			if request.method == 'POST':
				req: dict[str, any] = request.get_json()

				url: str = req.get('url')
				track: dict = req.get('track')

				if not url or not track:
					raise Status('No url or track provided', 400)


				audio, target_file_path = get_track(ydl, url, file_name, output_path, track, int(request.args.get('artworkSize', 1000)))
				audio.save()

				return {
					'fileName': target_file_path.name,
					'downloadUrl': request.root_url + str(target_file_path.as_posix())
				}

			# GET
			url = request.args.get('url')

			if not url:
				raise Status('No url provided', 400)

			info = ydl.extract_info(url, download=False)
			title = info.get('title') or info.get('fulltitle')
			artist = info.get('artist') or info.get('uploader')

			extracted = re.sub(r'\(official.+video\)', '', title, flags=re.IGNORECASE)
			extracted = re.sub(f'{artist.lower()} *- *', '', extracted, flags=re.IGNORECASE)

			upload_date = re.search(r'(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})', info.get('upload_date', ''))
			upload_date = upload_date.groupdict() if upload_date else {}

			upload_date_timestamp = datetime(int(upload_date.get('year', 0)), int(upload_date.get('month', 0)), int(upload_date.get('day', 0))).timestamp()
			return {
				'fullTitle': title,
				'title': extracted.strip(),
				'artist': artist,
				'url': url,
				'thumbnail': info.get('thumbnail'),
				'uploadDate': round(upload_date_timestamp * 1000, 0),
			}
	except Exception as e:
		Logger.log(traceback.format_exc(), log_type='ERROR')
		raise Status(str(e), 500)

def data(artist: str, title: str):
	def get_modifier(arg: str):
		modifiers = get_args(request, arg)

		modifiers = [mod for mod in modifiers if re.search(r'.+:.+', mod)]
		modifiers = { mod.split(':')[0]: mod.split(':')[1] for mod in modifiers }

		return modifiers

	lyrics_modifier = get_modifier('lyricsModifier')
	genres_modifier = get_modifier('genresModifier')
	excluded_genres = get_args(request, 'excludedGenres')
	included_genres = get_args(request, 'includedGenres')

	lyrics_provider = find_lyrics_provider(request.args.get('lyrics', 'AzLyrics').split(','), artist, title, lyrics_modifier)
	lyrics, lyrics_url = lyrics_provider.get(artist, title)


	genres_provider = Genre(
		excluded_genres=excluded_genres,
		included_genres=included_genres,
		modifiers=genres_modifier
	)

	genres, genres_url = genres_provider.get(artist, title)

	return { 'lyrics':  lyrics, 'lyricsUrl': lyrics_url, 'genres': [*genres], 'genresUrl': genres_url }

def downloads(path: str):
	return send_from_directory(output_path, path, as_attachment=True)