import logging
import spacy
from flask import Flask
from flask_cors import CORS
from flask_session import Session
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
import eventlet

import torch.nn as nn

class Net(nn.Module):
  """Class neural net with the architecture definition"""
  def __init__(self, input_size, hidden_size, output_size, n_layers, 
               bidirectional, dropout):
    super(Net, self).__init__()
    self.lstm = nn.LSTM(
      input_size, hidden_size, 
      num_layers=n_layers,
      bidirectional=bidirectional,
      dropout=dropout
    )

    self.head_layers = nn.Sequential(
      nn.Dropout(dropout),
      nn.Linear(2*hidden_size, hidden_size),
      nn.Dropout(dropout),
      nn.ReLU(),
      nn.Linear(hidden_size, output_size),
      nn.Dropout(dropout)
    )

  def forward(self, x):
    lstm_out, _ = self.lstm(x.view(len(x), 1, -1))
    x = self.head_layers(lstm_out.view(len(x), -1))
    return x

from config import Config

eventlet.monkey_patch()

sess = Session()
db = SQLAlchemy()

logger = logging.getLogger(__name__)

if Config.FLASK_ENV == 'production':
  logging.basicConfig(filename='server.log',level=logging.INFO)
  logging.basicConfig(filename='server.log',level=logging.ERROR)

app = Flask(__name__, instance_relative_config=False)

socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")

def create_app():
  app.config.from_object(Config)

  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  db.init_app(app)
  #db = SQLAlchemy(app)
  
  sess.init_app(app)

  CORS(app, resources={r"/api/*": { "origins": "*" } }, supports_credentials=True)

  from .routes import main
  from .routes import search
  from .routes import users

  app.register_blueprint(main.main_bp)
  app.register_blueprint(search.search_bp)
  app.register_blueprint(users.users_bp)
  
  return app
  