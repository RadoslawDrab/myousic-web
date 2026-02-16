from utils.track_data import Lyrics

class Lyrist(Lyrics):
	def __init__(self, modifiers: dict[str, str] = None) -> None:
		super().__init__(lyrics_url='https://lyrist.vercel.app/api', modifiers=modifiers)