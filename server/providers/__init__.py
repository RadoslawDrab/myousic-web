from providers.AzLyrics import AzLyrics
from providers.LyricsOvh import LyricsOvh
from providers.Lyrist import Lyrist
from providers.Genius import Genius
from utils.track_data import Lyrics
from type import LyricsProvider
from typing import overload, TypeVar

Provider = TypeVar('Provider', bound=Lyrics)

@overload
def map_provider(name: LyricsProvider | str) -> Provider | None: ...
@overload
def map_provider(name: LyricsProvider | str, default: Provider) -> Provider: ...
def map_provider(name: LyricsProvider | str, default: Provider | None = None):
	match name:
		case 'AzLyrics':
			return AzLyrics()
		case 'Lyrist':
			return Lyrist()
		case 'LyricsOvh':
			return LyricsOvh()
		case 'Genius':
			return Genius()
	return default