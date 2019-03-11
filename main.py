"""
The command line executable to analyze someone's Spotify library.
"""
import argparse
import sys
import math
import pathlib
import pickle

### Spotify-specific ###
import spotipy # Spotify API
import spotipy.util as util # for authorized requests

### In-House Imports ###
import years

AUTH_SCOPE = 'user-library-read'
CLIENT_ID = 'd4ce89eb38ee41c7836e9820875b6885'
CLIENT_SECRET = 'de5ca7b28c174d8ebe3fbcb2936e740c'
REDIRECT_URI = 'http://localhost/libraryanalysis/authenticate'

parser = argparse.ArgumentParser(description="Analyzes a Spotify library.")
parser.add_argument('-u', '--username', type=str, \
	help="The username of the Spotify library to be analyzed.")
parser.add_argument('-n', '--num-songs', type=int, default=300, \
	help="The number of songs from the Spotify library to analyze. The script considers the most recent n songs.")
parser.add_argument('-ny', '--no-years', action='store_true', default=True, \
	help="Doesn't analyze the year distribution of the songs in the library.")

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

if __name__ == '__main__':
	args = parser.parse_args(sys.argv[1:])

	# Initialize Spotipy
	username = _get_username(args.username)
	token = util.prompt_for_user_token(username, AUTH_SCOPE, client_id = CLIENT_ID, client_secret = CLIENT_SECRET, redirect_uri = REDIRECT_URI)

	if token:
		print("Authentication successful!")
		sp = spotipy.Spotify(auth=token)

		# Get the songs
		songs = _get_songs(sp, args.num_songs)

		# Get which functions of the program are enabled
		analyze_years = args.no_years

		if analyze_years:
			d = years.analyze(sp, songs)
			sorted_d = dict(sorted(d.items(), key=lambda x: x[0]))
			print(sorted_d)

	else:
		raise ValueError("The authentication was unsuccessful.")
