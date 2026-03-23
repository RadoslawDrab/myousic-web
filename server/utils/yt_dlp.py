import re
import uuid
from pathlib import Path

from yt_dlp import YoutubeDL

from utils.args import Args
from utils.conversion import validate_sample_rate


def get_yt_dlp(data: dict, output_path: Path | None = None):
	extension = data.get('extension', 'm4a')
	sample_rate = int(data.get('sampleRate', 48000))
	clipping = re.match(r'(?P<start>\d+),(?P<end>\d+)', data.get('clipping', ''))
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

	return YoutubeDL({
		'format': 'bestaudio/best',
		'outtmpl': file_name.stem + '.%(ext)s',
		'quiet': True,
		'postprocessors': [{  # Extract audio using ffmpeg
			'key': 'FFmpegExtractAudio',
			'preferredcodec': extension,
		}],
		'postprocessor_args': postprocessors_args,
		'paths': {
			'home': str(Args.output_path.joinpath(output_path) if output_path else Args.output_path),
			'temp': './.tmp'
		}
	}), file_name