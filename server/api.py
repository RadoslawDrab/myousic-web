import json
import traceback
from datetime import datetime
import re
import uuid
from pathlib import Path

from flask import request, send_from_directory

from providers import find_lyrics_provider
from utils import Status, get_args
from yt_dlp import YoutubeDL

from utils.args import Args
from utils.conversion import validate_sample_rate
from utils.logger import Logger
from utils.track import get_track
from utils.track_data import Genre, Lyrics

def api():
	try:
		extension = request.args.get('extension', 'm4a')
		sample_rate = int(request.args.get('sampleRate', 48000))
		clipping = re.match(r'(?P<start>\d+),(?P<end>\d+)', request.args.get('clipping', ''))
		if clipping: clipping = clipping.groupdict()

		sample_rate = validate_sample_rate(extension, sample_rate)

		id = uuid.uuid4()
		file_name = Path(f'{id}.{extension}')

		postprocessors_args = [
			'-ar', str(sample_rate),
		]

		if clipping:
			postprocessors_args.extend([
				'-ss', str(int(clipping.get('start', '0')) / 1000),
				'-to', str(int(clipping.get('end', '0')) / 1000)
			])

		ydl = YoutubeDL({
			'format': 'bestaudio/best',
			'outtmpl': file_name.stem + '.%(ext)s',
			'quiet': True,
			'postprocessors': [{  # Extract audio using ffmpeg
				'key': 'FFmpegExtractAudio',
				'preferredcodec': extension,
			}],
			'postprocessor_args': postprocessors_args,
			'paths': {
				'home': str(Args.output_path),
				'temp': str(Args.temp_path)
			}
		})

		with ydl:
			# POST
			if request.method == 'POST':
				body: dict[str, any] = json.loads(request.form.get('body', '{}'))

				url: str = body.get('url')
				track: dict = body.get('track')

				if not url or not track:
					raise Status('No url or track provided', 400)


				audio, target_file_path = get_track(
					ydl,
					url,
					Args.output_path.joinpath(file_name),
					track,
					artwork_size=int(request.args.get('artworkSize', 1000)),
					artwork_file=request.files.get('artworkFile')
				)
				audio.save()

				Logger.log(f'Audio "{target_file_path.name}" saved to "{Path.cwd().joinpath(target_file_path.parent).as_posix()}"', log_type='DEBUG', print_only=Args.dev)

				return {
					'fileName': target_file_path.name,
					'downloadUrl': '/audio/' + str(target_file_path.name)
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

			duration = info.get('duration_string')

			duration_match = re.match(r'(?P<hours>\d*?):?(?P<minutes>\d*?):?(?P<seconds>\d+?)$', str(duration)) if duration else None
			if duration_match:
				duration_times = duration_match.groupdict()
				duration = 0
				duration += int(duration_times.get('hours', 0) or 0) * 60 * 60 * 1000
				duration += int(duration_times.get('minutes', 0) or 0) * 60 * 1000
				duration += int(duration_times.get('seconds', 0) or 0) * 1000

			Logger.log(f'Audio data retrieved [{artist} - {extracted.strip()}]', log_type='DEBUG', print_only=Args.dev)

			return {
				'id': uuid.uuid4(),
				'fullTitle': title,
				'title': extracted.strip(),
				'artist': artist,
				'url': url,
				'artworkUrl': info.get('thumbnail'),
				'trackTimeMillis': 0 if type(duration) == str else duration,
				'releaseData': round(upload_date_timestamp * 1000, 0),
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

	Logger.log(f'Genres and lyrics retrieved [{artist} - {title}]', log_type='DEBUG', print_only=Args.dev)

	return { 'lyrics':  lyrics, 'lyricsUrl': lyrics_url, 'genres': [*genres], 'genresUrl': genres_url }

def downloads(path: str):
	return send_from_directory(Args.output_path, path, as_attachment=True)