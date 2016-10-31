from flask import Flask
from flask_bootstrap import Bootstrap
#from flask_pymongo import PyMongo 
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'my super secret key'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cwrbfaff:OfebqwY9QBEVmxKIlOdstOXCv_yeOGzp@tantor.db.elephantsql.com:5432/cwrbfaff' 
app.config['MONGO_HOST'] = 'ds137207.mlab.com'
app.config['MONGO_PORT'] = '37207'
app.config['MONGO_DBNAME'] = 'spotify'


#mongo = PyMongo(app)
db = SQLAlchemy(app)
from app import views
