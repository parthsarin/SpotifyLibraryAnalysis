#!/usr/bin/env python3
"""
The command line executable to analyze someone's Spotify library.
"""
import argparse
import sys
import math
import pathlib
import pickle
import collections

### Spotify-specific ###
import spotipy # Spotify API
import spotipy.util as util # for authorized requests

### In-House Imports ###
import years
import obscurity
import artists

AUTH_SCOPE = 'user-library-read'
CLIENT_ID = 'd4ce89eb38ee41c7836e9820875b6885'
CLIENT_SECRET = 'de5ca7b28c174d8ebe3fbcb2936e740c'
REDIRECT_URI = 'http://localhost/libraryanalysis/authenticate'

parser = argparse.ArgumentParser(description="Analyzes a Spotify library.")
parser.add_argument('-u', '--username', type=str, \
	help="The username of the Spotify library to be analyzed.")
parser.add_argument('-n', '--num-songs', type=int, default=300, \
	help="The number of songs from the Spotify library to analyze. The script considers the most recent n songs.")
parser.add_argument('-y', '--years', action='store_true', default=False, \
	help="Analyzes the year distribution of the songs in the library.")
parser.add_argument('--obscure', action='store_true', default=False, \
	help="Analyzes how obscure the songs in someone's library are.")
parser.add_argument('-a', '--artists', action='store_true', default=False, \
	help="Analyzes the artist distribution in someone's library.")
parser.add_argument('-o', metavar='FILENAME', type=str, \
	help="A file to print the output to.")

def _get_username(cmd_line_username):
	"""Gets the Spotify username for the user and stores
	it as a cached file.

	:cmd_line_username: The username passed in through the command line.
	:type cmd_line_username: str
	"""
	usernameFile = pathlib.Path(".cache-username")
	if usernameFile.is_file():
		with usernameFile.open('rb') as f:
			return pickle.load(f)
	elif cmd_line_username:
		with usernameFile.open('wb') as f:
			pickle.dump(cmd_line_username, f)
		return cmd_line_username
	else:
		username = input("Spotify username? ")
		with usernameFile.open('wb') as f:
			pickle.dump(username, f)
		return username

def _get_songs(sp, num_songs):
	"""Gets num_songs from the user's Spotify library.

	:sp: An authenticated Spotipy object.
	:type sp: spotipy.Spotify

	:num_songs: The number of songs to get.
	:type num_songs: int
	"""
	MAX_QUERY = 50
	queries = math.ceil(num_songs / MAX_QUERY)

	output = []

	for i in range(queries):
		query = sp.current_user_saved_tracks(limit=MAX_QUERY, offset=i*MAX_QUERY)

		if query['items']:
			output += query['items']
		else:
			# We've captured the entire library.
			return output

	return output[:num_songs]

def _write_to_file(string, file):
	"""Appends a string to a file.

	:string: The string to append.
	:file: A path to the file to append to.
	"""
	path = pathlib.Path(file)

	if not path.parent.exists():
		path.mkdir(parents=True)

	with path.open('w+') as f:
		f.write(string)

def table_to_str(title, headers, table, header_width=None):
	"""Converts a table to a string that can be written to a file.

	:title: The title of the table.
	:type title: str
	:headers: The headers in the table.
	:type headers: tuple
	:table: A table of information to be printed.
	:type table: dict or list of tuples
	:header_width: The width of each header entry.
	:type header_width: tuple
	"""
	# Calculate the width of each column
	widths = ()
	if header_width:
		widths = header_width
	else:
		for header in headers:
			widths += (len(header) + 1,)

	output = title + ':' + '\n' # The first line

	# Headers
	for i, header in enumerate(headers):
		if not i == len(headers)-1:
			output += ('{:' + str(widths[i]) + '} | ').format(header)
		else:
			output += ('{:' + str(widths[i]) + '}').format(header)
	output += '\n'

	# Horizontal line
	output += '-' * (sum(widths) + 3*(len(widths)-1)) + '\n'

	# Table entries
	items = table
	if type(table) == dict or type(table) == collections.defaultdict:
		items = table.items()

	for item in items:
		for i, field in enumerate(item):
			if not i == len(item)-1:
				output += ('{:' + str(widths[i]) + '} | ').format(field)
			else:
				output += ('{:' + str(widths[i]) + '}').format(field)
		output += '\n'

	return output

if __name__ == '__main__':
	args = parser.parse_args(sys.argv[1:])

	# Initialize Spotipy
	username = _get_username(args.username)
	token = util.prompt_for_user_token(username, AUTH_SCOPE, client_id = CLIENT_ID, client_secret = CLIENT_SECRET, redirect_uri = REDIRECT_URI)

	if token:
		sp = spotipy.Spotify(auth=token)

		# Get the songs
		songs = _get_songs(sp, args.num_songs)

		# Get the file to dump results to
		output_file = args.o

		# Get which functions of the program are enabled
		analyze_years = args.years
		analyze_obscurity = args.obscure
		analyze_artists = args.artists

		if analyze_years:
			d = years.analyze(sp, songs)
			sorted_d = dict(sorted(d.items(), key=lambda x: x[0]))

			printable_table = table_to_str("Year distribution", ("Year", "Number of Songs"), sorted_d)

			print(printable_table)
			if output_file:
				_write_to_file(printable_table, output_file)

		if analyze_obscurity:
			title, headers, distribution, header_width = obscurity.analyze(sp, songs)
			printable_table = table_to_str(title, headers, distribution, header_width=header_width)

			print(printable_table)
			if output_file:
				_write_to_file(printable_table, output_file)

		if analyze_artists:
			title, headers, distribution, header_width = artists.analyze(sp, songs)
			printable_table = table_to_str(title, headers, distribution, header_width=header_width)
			print(printable_table)

	else:
		raise ValueError("The authentication was unsuccessful.")
