from app import app
from flask import render_template
import requests
import asyncio
import aiohttp
import json
import time
import ast
import grequests
from pprint import pprint
DEBUG = False
REL_DEBUG = False
IMG_DEBUG = False
PREVIEW_DEBUG = True

# @asyncio.coroutine
# def do_work(task_name, work_queue):
#     while not workd_queue.empty():
#         queue_item = yield from work_queue.get()
#         print('{0} grabbed item: {1} from queue'.format(task_name, queue_item))
#         yield from asyncio.sleep(0.5)

# @asyncio.coroutine
# def get_related_artist_async(artist_id):
#     request_string = 'https://api.spotify.com/v1/artists/' + artist_id + '/related-artists'
#     response = yield from aiohttp.request('GET', request_strint)
#     related_artist_list = []
#     for artist in r.json()['artists']:
#         related_artist_list.append(artist['name'])


def get_related_artists(artist_id):
    if REL_DEBUG:
        start = time.time()
    request_string = 'https://api.spotify.com/v1/artists/' + artist_id + '/related-artists'
    r = requests.get(request_string)
    related_artist_list = []
    full_list = r.json()['artists']
    for artist in r.json()['artists']:
        related_artist_list.append(artist['name'])
    if REL_DEBUG:
        end = time.time()
        total_time = end - start
        print('get_related_artists took {} seconds'.format(total_time))
    # return [related_artist_list, request_string ]
    return full_list

def load_preview_track_url(artist_id):
    # payload = {'country': 'US'}
    return 'https://api.spotify.com/v1/artists/' + artist_id + '/top-tracks?country=US'

def get_preview_track(artist_id):
    if PREVIEW_DEBUG:
        start = time.time()
    payload = {'country': 'US'}
    request_string = 'https://api.spotify.com/v1/artists/' + artist_id + '/top-tracks'
    r = requests.get(request_string, params=payload)
    if PREVIEW_DEBUG:
        end = time.time()
        total_time = end - start
        print('get_preview_track took {} seconds'.format(total_time))

    return r.json()['tracks'][0]['preview_url']

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

@asyncio.coroutine
def get_artist_image_async(artist_id, image_num=1):
    request_string = requests.get('https://api.spotify.com/v1/artists/' + artist_id)
    image_list = r.json()['images']
    if len(image_list) <= 2:
        image_num = 1



def get_preview_tracks_async(preview_tracks):
    urls = preview_tracks
    rs = (grequests.get(u) for u in urls )
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

@app.route('/',methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/artist/<name>',methods=['GET', 'POST'])
def artist(name=""):
    if DEBUG:
        start = time.time()
    print( "name is: " , name)
    payload = {'q': name, 'type': 'artist'}
    r = requests.get('https://api.spotify.com/v1/search/', params=payload )
    artist_id = r.json()['artists']['items'][0]['id']
    if DEBUG:
        end = time.time()
        total_time = end - start
        print('artist took {} seconds'.format(total_time))
    return render_template('artist.html',name=name,id=artist_id ,image=get_artist_image(artist_id,image_num=1))

# @asyncio.coroutine
@app.route('/artist/related-artists/<name>')
def related_artists(name):
    if DEBUG:
        start = time.time()
    artist_image = []
    related_artists_ids = []
    related_artists = get_related_artists(get_artist_id(name))
    preview_track_urls = []
    # print("related_artists", related_artists)
   # queue = asyncio.Queue()
  #  tasks = [
  #      asyncio.async(do_work(get_artist_id(related_artist))),
  #      asyncio.async(do_work(related_artists_ids.append(rel_artist_id))),
  #      asyncio.aysnc(do_work(artist_image.append(get_artist_image(rel_artist_id, iamge_num=2)))),
  #      asyncio.aysnc(do_work(preview_tracks.append(get_preview_track(rel_artist_id))))]
   # loop.run_until_complete(asyncio.wait(tasks))
   # loop.close()


    for related_artist in related_artists:
        related_artists_ids.append(related_artist['id'])
        artist_image.append(related_artist['images'][1]['url'])
        preview_track_urls.append(load_preview_track_url(related_artist['id']))
        # artist_image.append(get_artist_image(rel_artist_id,image_num=2))
        # preview_tracks.append('https://api.spotify.com/v1/artists/' + related_artist['id'] + '/top-tracks?country=US')
        # preview_tracks.append(load_preview_track_url(related_artist['id']))


    preview_tracks = get_preview_tracks_async(preview_track_urls)
    #
    zipped_list = zip(related_artists, related_artists_ids, artist_image,preview_tracks)
    if DEBUG:
        end = time.time()
        total_time = end - start
        print('related_artists took {} seconds'.format(total_time))
    return render_template('related-artist.html', name=name, id=related_artists_ids, related=zipped_list)
