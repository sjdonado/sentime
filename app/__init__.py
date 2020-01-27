import logging
from flask import Flask
from flask_session import Session
from flask_socketio import SocketIO, emit

from config import Config

sess = Session()
logger = logging.getLogger(__name__)

if Config.FLASK_ENV == 'production':
  logging.basicConfig(filename='info.log',level=logging.INFO)

app = Flask(__name__, instance_relative_config=False)
socketio = SocketIO(app)

def create_app():
  app.config.from_object(Config)

  sess.init_app(app)

  from .routes import main
  from .routes import search

  app.register_blueprint(main.main_bp)
  app.register_blueprint(search.search_bp)
  
  return app
  