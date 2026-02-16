from utils.track_data import Lyrics

class LyricsOvh(Lyrics):
	def __init__(self, modifiers: dict[str, str] = None) -> None:
		super().__init__(lyrics_url='https://api.lyrics.ovh/v1', modifiers=modifiers)