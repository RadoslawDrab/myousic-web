import re
import urllib.request
from datetime import datetime
from pathlib import Path
import io
from pathvalidate import sanitize_filename

from PIL import Image
import music_tag
from werkzeug.datastructures import FileStorage
from yt_dlp import YoutubeDL

from utils import Status


def get_track(
	ydl: YoutubeDL,
	url: str,
	file_path: Path,
	track: dict,
	artwork_size: int = 1000,
	artwork_file: FileStorage | None = None
):
	ydl.extract_info(url, download=True)

	if not file_path.exists():
		raise FileNotFoundError(f'File "{file_path}" not found')


	target_file_path = file_path.parent.joinpath(sanitize_filename(f'{track.get('artistName', 'NONE')} - {track.get('trackName', 'NONE')}') + file_path.suffix)

	if target_file_path.exists():
		target_file_path.unlink()

	file_path.rename(target_file_path)

	audio = music_tag.load_file(target_file_path)


	if artwork_file:
		artwork_file_path = target_file_path.parent.joinpath(f'{target_file_path.stem}.jpeg')
		artwork_file.save(artwork_file_path)
		get_artwork(artwork_file, artwork_file_path)
	else:
		artwork_url = re.sub(r'\d+x\d+b', f'{artwork_size}x{artwork_size}b', track.get('artworkUrl100', ''))
		artwork_file_path = target_file_path.parent.joinpath(f'{target_file_path.stem}.jpeg')
		get_artwork(artwork_url, artwork_file_path)

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
	}

	for audio_key, track_key in mapped.items():
		audio[audio_key] = track.get(track_key)

	if artwork_file_path.exists():
		with open(artwork_file_path, 'rb') as f:
			audio['artwork'] = f.read()

	release_date = track.get('releaseDate')
	if release_date:
		audio['year'] = datetime.fromisoformat(release_date).year

	return audio, target_file_path


def get_artwork(url_or_file: str | FileStorage, file_path: Path):
	if isinstance(url_or_file, str):
		with urllib.request.urlopen(url_or_file) as url_img:
			# Load the image into memory first
			img_data = url_img.read()
	elif isinstance(url_or_file, FileStorage):
		url_or_file.seek(0)
		img_data = url_or_file.stream.read()

	img = Image.open(io.BytesIO(img_data))

	# Convert to RGB (removes alpha channel if source was PNG)
	if img.mode in ("RGBA", "P"):
		img = img.convert("RGB")

	# Save as JPEG to the file path
	# Even if path ends in .png, saving as JPEG clarifies headers
	img.save(file_path, format='JPEG', quality=95)

	return img