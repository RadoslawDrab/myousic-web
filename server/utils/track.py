import re
import urllib.request
from datetime import datetime
from pathlib import Path
import io
from pathvalidate import sanitize_filename

from PIL import Image
import music_tag
from yt_dlp import YoutubeDL

from utils import Status

def get_track(ydl: YoutubeDL, url: str, file_name: str, output_path: Path, track: dict, artwork_size: int = 1000):
	info = ydl.extract_info(url, download=True)
	ext = info.get('audio_ext')
	file_path = output_path.joinpath(file_name)

	if not file_path.exists():
		raise Status('File not found', 404)

	target_file_path = output_path.joinpath(sanitize_filename(f'{track.get('artistName', 'NONE')} - {track.get('trackName', 'NONE')}') + f'.{ext}')

	if target_file_path.exists():
		target_file_path.unlink()

	file_path.rename(target_file_path)

	audio = music_tag.load_file(target_file_path)


	artwork_url = re.sub(r'\d+x\d+b', f'{artwork_size}x{artwork_size}b', track.get('artworkUrl100', ''))
	artwork_file = target_file_path.parent.joinpath(f'{target_file_path.stem}.jpeg')

	get_artwork(artwork_url, artwork_file)

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

	if artwork_url:
		with open(artwork_file, 'rb') as f:
			audio['artwork'] = f.read()

	release_date = datetime.fromisoformat(track.get('releaseDate'))
	if release_date:
		audio['year'] = release_date.year

	return audio, target_file_path


def get_artwork(url: str, file_path: Path):
	with urllib.request.urlopen(url) as url_img:
		# Load the image into memory first
		img_data = url_img.read()
		img = Image.open(io.BytesIO(img_data))

		# Convert to RGB (removes alpha channel if source was PNG)
		if img.mode in ("RGBA", "P"):
			img = img.convert("RGB")

		# Save as JPEG to the file path
		# Even if path ends in .png, saving as JPEG clarifies headers
		img.save(file_path, format='JPEG', quality=95)

		return img