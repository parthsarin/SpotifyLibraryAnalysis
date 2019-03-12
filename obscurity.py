"""
Analyzes how obscure the songs in someone's library are.
"""
import matplotlib.pyplot as plt
import collections

def analyze(sp, songs, granularity=10):
	distribution = collections.defaultdict(int)
	song_popularities = {}

	# Loop over the songs, building a distribution and keeping track of their popularities
	longest_name = ""
	for song in songs:
		song = song['track']

		# Update longest name
		if len(song['name']) > len(longest_name):
			longest_name = song['name']

		# Update distribution and save song
		distribution[song['popularity']] += 1
		song_popularities[song['name']] = song['popularity']

	# Display a bar graph with the year and number of songs.
	plt.bar(distribution.keys(), height=distribution.values())

	min_pop = min(distribution.keys())
	max_pop = max(distribution.keys())
	if max_pop - min_pop >= 20:
		plt.xticks(range(min_pop, max_pop+5, 5))

	plt.xlabel('Popularity')
	plt.ylabel('Number of songs')
	plt.show()

	# Table data for return
	title = "Song Popularity"
	headers = ('Name', 'Popularity')
	header_width = (len(longest_name)+3, 10)
	song_popularities = dict(sorted(song_popularities.items(), key=lambda x: x[1])) # sort by popularity

	return title, headers, song_popularities, header_width