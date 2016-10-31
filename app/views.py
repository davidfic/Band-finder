from app import app
from flask import render_template, request
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from pymongo import MongoClient
from flask_sqlalchemy import SQLAlchemy
from models import User, Role
from forms import NameForm

import requests
import json
import time
import grequests
# from pprint import pprint
DEBUG = False
REL_DEBUG = False
IMG_DEBUG = False
PREVIEW_DEBUG = True

@app.route('/form', methods=['GET', 'POST'])
def form_test():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        password = form.password.data
        name = form.name.data
        print 'name from for is', name
        print 'password is', password
        form.name.data = ''
    return render_template('login.html', form=form, name=name)
    
def mongo_client():
    client = MongoClient("ds137207.mlab.com", 37207)
    client.spotify.authenticate('david', 'password123')
    db = client['spotify']
    return db

def postgress_client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cwrbfaff:OfebqwY9QBEVmxKIlOdstOXCv_yeOGzp@tantor.db.elephantsql.com:5432/cwrbfaff' 
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
#    r = requests.get('https://api.spotify.com/v1/search/', params=payload)
    artist_id = get_artist_id(name)
#    print('artist id is {}'.format(artist_id))
    r = requests.get('https://api.spotify.com/v1/artists/' + artist_id) 
    album_request_string = 'https://api.spotify.com/v1/artists/' + artist_id + '/albums'
#    print 'album_request_string is: ', album_request_string

    album_request = requests.get(album_request_string)
    album_list = []
#    print(r.json())
    for album in album_request.json()['items']:
#        print album['name']
        if album['name'] not in album_list:
            album_list.append(album['name'])

    popularity = r.json()['popularity']
    followers = r.json()['followers']['total']
    open_link = r.json()['external_urls']['spotify']
#    print('open_link is {}'.format( open_link))
#    print('followers is {}'.format( followers))
#    print('artist image url: {}'.format(get_artist_image(artist_id)))
    if DEBUG:
        end = time.time()
        total_time = end - start
#        print('artist took {} seconds'.format(total_time))
    return render_template('artist.html',
                           name=name,
                           id=artist_id,
                           followers=followers,
                           pop=popularity,
                           open_link=open_link,
                           album_list=album_list,
                           image=get_artist_image(artist_id, image_num=1))


@app.route('/mongotest/<data>')
def mongo_test(data):
    
    db = mongo_client()

    try:
        result = db.test.insert_one( { "address": data } )
    except Exception as e:
        print(e)
    return data

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

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
