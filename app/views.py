from app import create_app
from flask import render_template

app = create_app()
import spotipy
sp = spotipy.Spotify()
from pprint import pprint

def get_related_artists(artist_id):
    related_artists = sp.artist_related_artists(artist_id)
    related_artist_list = []
    for artist in related_artists['artists']:
        related_artist_list.append(artist['name'])


    return related_artist_list

def get_related_related(artist_id):
    related_artists = sp.artists_related_artists(artist_id)
    related_related_artist_list = []
    for artist in related_related_artist_list['artists']:
        related_related_artist_list.append(artist['name'])

    return related_related_artist_list

def get_artist_id(artist_name):
    artist_id = sp.search(artist_name,type='artist')
    # print artist_id['artists']['items'][0]['id']
    return artist_id['artists']['items'][0]['id']

def get_artist_image(artist_id):
    results = sp.artist(artist_id)
    return results['images'][2]['url']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/artist/<name>')
def artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    artist_id = results['artists']['items'][0]['id']

    return render_template('artist.html',name=name,id=artist_id)#, related=zipped_list)

@app.route('/artist/related-artist/<name>')
def related_artists(name):
    results = sp.search(q='artist:' + name, type='artist')
    artist_id = results['artists']['items'][0]['id']

    artist_image = []
    related_artists_ids = []
    related_artists = get_related_artists(artist_id)
    for artist in related_artists:
        related_artists_ids.append(get_artist_id(artist))
        artist_image.append(get_artist_image(get_artist_id(artist)))

    zipped_list = zip(related_artists, related_artists_ids, artist_image)
    return render_template('related-artist.html', name=name, id=artist_id, related=zipped_list)
