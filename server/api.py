import urllib
from datetime import datetime
import re
import uuid
from pathlib import Path
import music_tag

from flask import request, send_from_directory

from providers import map_provider
from utils import Status, get_args
from yt_dlp import YoutubeDL

from utils.track_data import Genre, Lyrics


audio_path = Path('./audio')
temp_path = Path('./temp')

audio_path.mkdir(exist_ok=True)

def api():
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
			'home': str(audio_path),
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

			info = ydl.extract_info(url, download=True)
			ext = info.get('audio_ext')
			file_path = audio_path.joinpath(file_name)

			if not file_path.exists():
				raise Status('File not found', 404)

			target_file_path = audio_path.joinpath(f'{track.get('artistName')} - {track.get('trackName')}.{ext}')

			if target_file_path.exists():
				target_file_path.unlink()

			file_path.rename(target_file_path)

			audio = music_tag.load_file(target_file_path)

			artwork_url = re.sub(r'\d+x\d+b', '1000x1000b', info.get('artworkUrl100', ''))
			artwork_filename = target_file_path.parent.joinpath(f'{target_file_path.stem}.jpg')

			if artwork_url:
				# Saves artwork in temp file
				with urllib.request.urlopen(artwork_url) as url:
					with open(artwork_filename, 'wb') as f:
						f.write(url.read())

			mapped = {
				'title': 'trackName',
				'artist': 'artistName',
				'composer': 'artistName',
				'album-artist': 'artistName',
				'album': 'collectionName',
				'genre': 'primaryGenreName',
				'track-number': 'trackNumber',
				'total-tracks': 'trackCount',
				'disc-number': 'discNumber',
				'total-discs': 'diskCount',
				'lyrics': 'lyrics',
				'comment': 'comment'
				# 'year': 'releaseDate'
			}

			for audio_key, track_key in mapped.items():
				audio[audio_key] = track.get(track_key)

			if artwork_url:
				with open(artwork_filename, 'rb') as f:
					audio['artwork'] = f.read()

			release_date = datetime.fromisoformat(track.get('releaseDate'))
			if release_date:
				audio['year'] = release_date.year

			# audio['comment'] = f'[URL: {url}]'

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

	lyrics_provider = map_provider('AzLyrics' or request.args.get('lyrics', 'AzLyrics'))
	lyrics_provider.modifiers = lyrics_modifier
	lyrics, lyrics_url = lyrics_provider.get_to_file(str(audio_path.joinpath(f'{artist} - {title}.txt')), artist, title)


	genres_provider = Genre(
		excluded_genres=excluded_genres,
		included_genres=included_genres,
		modifiers=genres_modifier
		# modifiers={ value.split(':')[0]: value.split(':')[1] for value in request.args.get('modifiers', '').split(',') }
	)

	genres, genres_url = genres_provider.get(artist, title)

	return { 'lyrics':  lyrics, 'lyricsUrl': lyrics_url, 'genres': [*genres], 'genresUrl': genres_url }
	...

def downloads(path: str):
	return send_from_directory(audio_path, path, as_attachment=True)