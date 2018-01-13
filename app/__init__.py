from flask import Flask
from flask_bootstrap import Bootstrap



def create_app():
    app = Flask(__name__)
    # app.config.from_pyfile(config_filename)

    # from yourapplication.model import db
    # db.init_app(app)

    # from yourapplication.views.admin import admin
    # from yourapplication.views.frontend import frontend
    # app.register_blueprint(admin)
    # app.register_blueprint(frontend)
    Bootstrap(app)

    return app

# app = Flask(__name__)


from app import views
