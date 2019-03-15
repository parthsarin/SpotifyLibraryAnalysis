"""
Analyzes the distribution of artists in your library.
"""
import collections
import sys
import matplotlib.pyplot as plt

def analyze(sp, songs):
	"""Gives a distribution of the artists in someone's library.

	:sp: An authenticated Spotipy object.
	:type sp: spotipy.Spotify
	:songs: A list of Spotify songs to analyze.
	"""
	distribution = collections.defaultdict(int)
	largest_name = 0

	for song in songs:
		song = song['track']

		for artist in song['artists']:
			distribution[artist['name']] += 1

			if len(artist['name']) > largest_name:
				largest_name = len(artist['name'])

	sorted_d = dict(sorted(distribution.items(), key=lambda x: x[1]))

	title = "Artist distribution"
	headers = ("Artist", "Number of Songs")
	table = sorted_d
	header_width = (largest_name+1, 13)

	return title, headers, table, header_width
		