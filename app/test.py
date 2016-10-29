from pymongo import MongoClient
from flask_sqlalchemy import SQLAlchemy

client = MongoClient("ds137207.mlab.com", 37207)
client.spotify.authenticate('david', 'password123')


db = client['spotify']

try:
    result = db.test.insert_one( { "address": "test" } )
except Exception as e:
    print(e)


