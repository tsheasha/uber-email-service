from flask import Flask

from . import settings
from index import index_blueprint
from mail_dispatcher import mail_dispatcher_blueprint

from flask.ext.heroku import Heroku
from flask.ext.compress import Compress
 
def create_app(priority_settings=None):
    
    # Initialising a Flask App
    app = Flask(__name__, static_url_path='')
    heroku = Heroku()
    compress = Compress() 

    # Load configuraiton from settings file
    app.config.from_object(settings)
    app.config.from_object(priority_settings)

    # Using Heroku as deployment server
    heroku.init_app(app)
    
    # Gziping responses from app
    compress.init_app(app)
    
    # Registering Blueprints in an effort to make app modular
    app.register_blueprint(index_blueprint)
    app.register_blueprint(mail_dispatcher_blueprint)

    return app
