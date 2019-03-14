# Spotify Library Analysis

This project contains Python files that will analyze a user's Spotify library on a variety of metrics including the years that their songs were written and the popularity of songs they listen to. This project is dedicated to embarrasing Jade.

In order to allow the program to authenticate with Spotify, you will need to install the `spotipy` module for Python. You can install the latest version with the command:

```
pip install git+https://github.com/plamere/spotipy.git --upgrade
```

The program can be run as a shell script and `python main.py -h` prints out the help page:

```
usage: main.py [-h] [-u USERNAME] [-n NUM_SONGS] [-y] [--obscure]
               [-o FILENAME]

Analyzes a Spotify library.

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        The username of the Spotify library to be analyzed.
  -n NUM_SONGS, --num-songs NUM_SONGS
                        The number of songs from the Spotify library to
                        analyze. The script considers the most recent n songs.
  -y, --years           Analyzes the year distribution of the songs in the
                        library.
  --obscure             Analyzes how obscure the songs in someone's library
                        are.
  -o FILENAME           A file to print the output to.
```

The first time you run the program with a nontrivial flag, it will prompt you for your username (unless you've provided it as a command line argument) and store that value locally. Then it should redirect you to a web browser where you can authenticate with Spotify. Once authenticated, you will be redirected to a `localhost` address that will probably not load. You should paste the url you are redirected to into the terminal. This authenticates the program with Spotify.

After that, the program will display bar graphs and print output to the terminal containing the analysis of your spotify library.