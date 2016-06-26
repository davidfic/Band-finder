from app import app
from flask import render_template
import requests

import spotipy
sp = spotipy.Spotify()
from pprint import pprint

def get_related_artists(artist_id):
    request_string = 'https://api.spotify.com/v1/artists/' + artist_id + '/related-artists'
    r = requests.get(request_string)
    related_artist_list = []
    for artist in r.json()['artists']:
        related_artist_list.append(artist['name'])

    return related_artist_list

def get_preview_track(artist_id):
    payload = {'country': 'US'}
    request_string = 'https://api.spotify.com/v1/artists/' + artist_id + '/top-tracks'
    r = requests.get(request_string, params=payload)
    return r.json()['tracks'][0]['preview_url']

def get_artist_id(artist_name):
    payload = {'q': artist_name, 'type': 'artist'}
    r = requests.get("https://api.spotify.com/v1/search", params=payload)
    # get json format from response and extract ID
    return r.json()['artists']['items'][0]['id']

def get_artist_image(artist_id, image_num=1):
    r = requests.get('https://api.spotify.com/v1/artists/' + artist_id)
    image_list = r.json()['images']
    if len(image_list) <= 2:
        image_num = 1
    return r.json()['images'][image_num]['url']

@app.route('/',methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/artist/<name>',methods=['GET', 'POST'])
def artist(name=""):
    print "name is: " , name
    results = sp.search(q='artist:' + name, type='artist')
    artist_id = results['artists']['items'][0]['id']
    return render_template('artist.html',name=name,id=artist_id ,image=get_artist_image(artist_id,image_num=1))

@app.route('/artist/related-artist/<name>')
def related_artists(name):
    results = sp.search(q='artist:' + name, limit=4, type='artist' )
    artist_id = results['artists']['items'][0]['id']

    artist_image = []
    related_artists_ids = []
    preview_tracks = []
    related_artists = get_related_artists(artist_id)
    for related_artist in related_artists:
        rel_artist_id = get_artist_id(related_artist)
        related_artists_ids.append(rel_artist_id)
        artist_image.append(get_artist_image(rel_artist_id,image_num=2))
        preview_tracks.append(get_preview_track(rel_artist_id))

    zipped_list = zip(related_artists, related_artists_ids, artist_image,preview_tracks)
    return render_template('related-artist.html', name=name, id=artist_id, related=zipped_list)
