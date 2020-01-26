import logging
from config import Config
from flask import Flask
from flask_session import Session

global logger

sess = Session()
logger = logging.getLogger(__name__)

if Config.FLASK_ENV == 'development':
  logging.basicConfig(filename='info.log',level=logging.INFO)

app = Flask(__name__, instance_relative_config=False)

def create_app():
  app.config.from_object(Config)

  sess.init_app(app)

  with app.app_context():
    from .routes import search
    from .routes import main
    app.register_blueprint(main.main_bp)
    app.register_blueprint(search.search_bp)

    return app