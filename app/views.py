from app import app
from flask import render_template


import spotipy
sp = spotipy.Spotify()
from pprint import pprint

def get_related_artists(artist_id):
    related_artists = sp.artist_related_artists(artist_id)
    related_artist_list = []
    for artist in related_artists['artists']:
        related_artist_list.append(artist['name'])


    return related_artist_list

def get_preview_track(artist_id):
    track = sp.artist_top_tracks(artist_id, country='US')
    # pprint(track)
    return track['tracks'][0]['preview_url']

def get_artist_id(artist_name):
    artist_id = sp.search(artist_name,type='artist')
    # print artist_id['artists']['items'][0]['id']
    return artist_id['artists']['items'][0]['id']

def get_artist_image(artist_id, image_num=1):
    results = sp.artist(artist_id)
    image_list = results['images']
    if len(image_list) <= 2:
        image_num = 1
    print artist_id
    print "results are:" ,results['images'][image_num]['url']
    return results['images'][image_num]['url']

@app.route('/',methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/artist/?<name>',methods=['GET', 'POST'])
# @app.route('/artist/<name>', methods=['GET', 'POST'])
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
