import re

import requests
from flask import request

from . import api
from utils.args import Args
from utils import Status, get_args, get_env
from utils.logger import Logger
from utils.track_data import Genre
from providers import find_lyrics_provider

ITUNES_URL = get_env('SERVER_ITUNES_URL', default='https://itunes.apple.com/search')

@api.route("/track-data", methods=["GET"])
def get_tracks():

	term = request.args.get('term')
	entity = request.args.get('entity')
	country = request.args.get('country', 'US')
	explicit = request.args.get('explicit')
	limit = request.args.get('limit', 200)

	if not term:
		raise Status('No term provided', 400)

	params = {
		"term": term,
		"country": country,
		"limit": limit,
		"lang": "en_us"
	}
	if entity: params['entity'] = entity
	if explicit: params['explicit'] = 'Yes' if explicit == 'true' else 'No'

	try:
		response = requests.get(ITUNES_URL, params=params, timeout=10)
		response.raise_for_status()

		return response.json()
	except requests.exceptions.RequestException as e:
		Logger.log(f'Error fetching tracks: {str(e)}', log_type='ERROR')
		raise Status(str(e), 500)

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
	lyrics, lyrics_url = lyrics_provider.get(artist, title) if lyrics_provider else (None, None)

	Logger.log(f'Lyrics {'' if lyrics else 'not '}retrieved [{artist} - {title}]', log_type='DEBUG', print_only=Args.dev)


	genres_provider = Genre(
		excluded_genres=excluded_genres,
		included_genres=included_genres,
		modifiers=genres_modifier
	)

	genres, genres_url = genres_provider.get(artist, title) if genres_provider else (None, None)

	Logger.log(f'Genres {'' if genres else 'not '}retrieved [{artist} - {title}]', log_type='DEBUG', print_only=Args.dev)

	return { 'lyrics':  lyrics, 'lyricsUrl': lyrics_url, 'genres': [*(genres or [])], 'genresUrl': genres_url }