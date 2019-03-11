"""
Analyzes the year-release distribution of the songs
in someone's Spotify library.
"""
import collections
import matplotlib.pyplot as plt

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

	# Display a bar graph with the year and number of songs.
	plt.bar(distribution.keys(), height=distribution.values())

	min_year = min(distribution.keys())
	max_year = max(distribution.keys())
	if max_year-min_year >= 20:
		plt.xticks(range(min_year, max_year+5, 5))

	plt.xlabel('Year')
	plt.ylabel('Number of songs')
	plt.show()

	return distribution