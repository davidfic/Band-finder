from app import app
from flask import render_template, request
import requests
import json
import time
import grequests
from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# client_credentials_manager = SpotifyClientCredentials()
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
# from pprint import pprint
DEBUG = False
REL_DEBUG = False
IMG_DEBUG = False
PREVIEW_DEBUG = True

    
client_credentials_manager = SpotifyClientCredentials()
spotipy_client = spotipy.Spotify(client_credentials_manager=client_credentials_manager)



def get_related_artists(artist_id):

    
    if REL_DEBUG:
        start = time.time()
    artist = spotipy_client.artist(artist_id)
    related_artists = spotipy_client.artist_related_artists(artist_id)
    
    # request_string = 'https://api.spotify.com/v1/artists/' \
    #     + artist_id \
    #     + '/related-artists'

    # r = requests.get(request_string)
    # related_artist_list = []
    if DEBUG:
        for artist in related_artists['artists']:
            print('artist name is: {}'.format(artist['name']))
    # full_list = r.json()['artists']
    # for artist in r.json()['artists']:
    #     related_artist_list.append(artist['name'])
    # if REL_DEBUG:
    #     end = time.time()
    #     total_time = end - start
    #     print('get_related_artists took {} seconds'.format(total_time))
    # return full_list
    return related_artists

def load_preview_track_url(artist_id):
    # payload = {'country': 'US'}
    tracks = spotipy_client.artist_top_tracks(artist_id, country='US')
    top_tracks = []
    count = 0
    for track in tracks['tracks']:
        if count > 0:
            break
        if track['preview_url'] is not None:
            count += 1
            print('adding {} to top_tracks'.format(track['preview_url']))
            top_tracks.append(track['preview_url'])
        else:
            top_tracks.append(" ")
    
    print('length of top_tracks is {}'.format(len(top_tracks)))
    if len(top_tracks) > 0:
        return top_tracks[0]
    return top_tracks


def get_artist_id(artist_name):
    """
    return the Spotify ID of the given artist name
    """
    artist = spotipy_client.search(artist_name, type='artist')
    return artist['artists']['items'][0]['id']


def get_preview_tracks_async(preview_tracks):
    urls = preview_tracks
    print('in async preview_tracks are {}'.format(preview_tracks))
    rs = (grequests.get(u) for u in urls)
    preview_urls = []
    for response in grequests.map(rs):
        str_resp = response.content.decode("utf-8")
        json_data = json.loads(str_resp)
        preview_urls.append(json_data['tracks'][0]['preview_url'])
    return preview_urls


def get_artist_image(artist_id, image_num=1):
    if IMG_DEBUG:
        start = time.time()
    id_get_start = time.time()
    if DEBUG:
        print('url is {}'.format(spotipy_client.artist(artist_id)['images'][0]['url']))
    
    return spotipy_client.artist(artist_id)['images'][0]['url']


@app.route('/')#, methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/artist', methods=['GET', 'POST'])
# @app.route('/artist/<name>', methods=['GET', 'POST'])
def artist():
    result = ""
    if DEBUG:
        start = time.time()
    if request.method == 'POST':
        result = request.form['name']

    artist_id = get_artist_id(result)
    artist = spotipy_client.artist(artist_id)
    artist_albums = spotipy_client.artist_albums(artist_id,country='US')
    album_list = []

    popularity = artist['popularity']
    followers = artist['followers']
    open_link = artist['external_urls']['spotify']
    if DEBUG:
        end = time.time()
        total_time = end - start
    if DEBUG:
        for item in artist_albums['items']:
            print("item is {}".format(item))
    return render_template('artist.html',
                           name=artist['name'],
                           id=artist_id,
                           followers=followers,
                           pop=popularity,
                           open_link=open_link,
                           album_list=artist_albums['items'],
                           image=get_artist_image(artist_id, image_num=1))


@app.route('/related-artists/<name>')
def related_artists(name):
    artist_image = []
    related_artists_ids = []
    preview_track_urls = []
    name_list = []

    artist_id = get_artist_id(name)
    print(artist_id)
    related_artists = get_related_artists(get_artist_id(name))
    
    for related_artist in related_artists['artists']:
        name_list.append(related_artist['name'])
        related_artists_ids.append(related_artist['id'])
        artist_image.append(related_artist['images'][1]['url'])
        preview_track_urls.append(load_preview_track_url(related_artist['id']))
    # preview_tracks = get_preview_tracks_async(preview_track_urls)

    zipped_list = zip(name_list,
                      related_artists_ids,
                      artist_image,
                      preview_track_urls)
                    

    if DEBUG:
        print('related_artists took {} seconds'.format(total_time))

    return render_template('related-artist.html',
                           name=name,
                           id=related_artists_ids,
                           related=zipped_list)
                           
