
LIMITS = {
	'mp3': 48000,
	'opus': 48000,
	'm4a': 96000,
	'wav': 192000,
	'flac': 192000
}

def validate_sample_rate(ext: str, rate: int):
	max_rate = LIMITS.get(ext.lower(), 48000)
	return min(int(rate), max_rate)