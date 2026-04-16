import re

from flask import request

from . import api
from utils.args import Args
from utils import get_args
from utils.logger import Logger
from utils.track_data import Genre
from providers import find_lyrics_provider


@api.route("/track-data/<string:artist>/<string:title>", methods=["GET"])
def track_data(artist: str, title: str):
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
	lyrics, lyrics_url = lyrics_provider.get(artist, title) if lyrics_modifier else (None, None)

	Logger.log(f'Lyrics {'' if lyrics else 'not '}retrieved [{artist} - {title}]', log_type='DEBUG', print_only=Args.dev)


	genres_provider = Genre(
		excluded_genres=excluded_genres,
		included_genres=included_genres,
		modifiers=genres_modifier
	)

	genres, genres_url = genres_provider.get(artist, title) if genres_modifier else (None, None)

	Logger.log(f'Genres {'' if genres else 'not '}retrieved [{artist} - {title}]', log_type='DEBUG', print_only=Args.dev)

	return { 'lyrics':  lyrics, 'lyricsUrl': lyrics_url, 'genres': [*genres], 'genresUrl': genres_url }