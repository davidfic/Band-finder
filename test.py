import spotipy
sp = spotipy.Spotify()
from pprint import pprint

results = sp.search(q='beck', limit=1)
pprint (results['tracks']['items'][0]['id'])

