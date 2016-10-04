from app import app
from flask import render_template, request
import requests
import json
import time
import grequests
# from pprint import pprint
DEBUG = False
REL_DEBUG = False
IMG_DEBUG = False
PREVIEW_DEBUG = True


def get_related_artists(artist_id):

    if REL_DEBUG:
        start = time.time()
    request_string = 'https://api.spotify.com/v1/artists/' \
        + artist_id \
        + '/related-artists'

    r = requests.get(request_string)
    related_artist_list = []
    full_list = r.json()['artists']
    for artist in r.json()['artists']:
        related_artist_list.append(artist['name'])
    if REL_DEBUG:
        end = time.time()
        total_time = end - start
        print('get_related_artists took {} seconds'.format(total_time))
    return full_list


def load_preview_track_url(artist_id):
    # payload = {'country': 'US'}
    return 'https://api.spotify.com/v1/artists/' \
        + artist_id \
        + '/top-tracks?country=US'


def get_artist_id(artist_name):
    if DEBUG:
        start = time.time()
    payload = {'q': artist_name, 'type': 'artist'}

    r = requests.get("https://api.spotify.com/v1/search", params=payload)
    # get json format from response and extract ID
    if DEBUG:
        end = time.time()
        total_time = end - start
        print('get_artist_id took {} seconds'.format(total_time))
    return r.json()['artists']['items'][0]['id']


def get_preview_tracks_async(preview_tracks):
    urls = preview_tracks
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
    r = requests.get('https://api.spotify.com/v1/artists/' + artist_id)
    id_get_stop = time.time()
    print('artist_id get took {} seconds'.format(id_get_stop - id_get_start))
    image_list = r.json()['images']
    if len(image_list) <= 2:
        image_num = 1
    if IMG_DEBUG:
        end = time.time()
        total_time = end - start
        print('get_artist_image took {} seconds'.format(total_time))

    return r.json()['images'][image_num]['url']


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/artist', methods=['GET', 'POST'])
# @app.route('/artist/<name>', methods=['GET', 'POST'])
def artist(name=""):
    if DEBUG:
        start = time.time()
    if request.method == 'POST':
        result = request.form['name']
    name = result
    payload = {'q': name, 'type': 'artist'}
    r = requests.get('https://api.spotify.com/v1/search/', params=payload)
    artist_id = r.json()['artists']['items'][0]['id']
    if DEBUG:
        end = time.time()
        total_time = end - start
        print('artist took {} seconds'.format(total_time))
    return render_template('artist.html',
                           name=name,
                           id=artist_id,
                           image=get_artist_image(artist_id, image_num=1))


@app.route('/related-artists/<name>')
def related_artists(name):

    print "received the name: {} from call".format(name)

    if DEBUG:
        start = time.time()

    artist_image = []
    related_artists_ids = []
    preview_track_urls = []
    name_list = []

    related_artists = get_related_artists(get_artist_id(name))

    for related_artist in related_artists:
        related_artists_ids.append(related_artist['id'])
        artist_image.append(related_artist['images'][1]['url'])
        preview_track_urls.append(load_preview_track_url(related_artist['id']))

    for item in related_artists:
        name_list.append(item['name'])

    preview_tracks = get_preview_tracks_async(preview_track_urls)

    zipped_list = zip(name_list,
                      related_artists_ids,
                      artist_image, preview_tracks)

    if DEBUG:
        end = time.time()
        total_time = end - start
        print('related_artists took {} seconds'.format(total_time))

    return render_template('related-artist.html',
                           name=name,
                           id=related_artists_ids,
                           related=zipped_list)
