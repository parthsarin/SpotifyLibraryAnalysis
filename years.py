"""
Analyzes the year-release distribution of the songs
in someone's Spotify library.
"""
import collections

def analyze(sp, songs):
	"""Gives a year-breakdown of the songs in someone's
	library.

	:sp: An authenticated Spotipy object.
	:type sp: spotipy.Spotify
	:songs: A list of Spotify songs to analyze.
	"""
	distribution = collections.defaultdict(int)

	for song in songs:
		year = int(song['track']['album']['release_date'][:4])
		distribution[year] += 1

	return distribution