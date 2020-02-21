import os
import csv
import json

import twint
import asyncio
import threading

from flask import session, Blueprint

from .. import socketio, app

cities_path =  os.path.join(app.static_folder, 'data', 'Departamentos_y_municipios_de_Colombia.csv')
cities = []

for row in csv.DictReader(cities_path):
  cities.append(json.dumps(row))

# Blueprint Configuration
search_bp = Blueprint('search_bp', __name__,
                      template_folder='templates',
                      static_folder='static')

def launch_query(c):
  asyncio.set_event_loop(asyncio.new_event_loop())
  twint.run.Search(c)

  tweets = [t.__dict__ for t in twint.output.tweets_list]
  # print("DATA => {}".format(tweets), flush=True)
  socketio.emit('tweets', { 'message': 'Finished', 'data': tweets })

@socketio.on('search')
def search(message):
  data = json.loads(message)

  # TODO:
  # Connect to geocode to get the coordinates for a city
  # Get tweets by cities

  session['text'] = data['text']
  c = twint.Config()
  c.Search = data['text']
  c.Store_object = True
  c.Location = True
  c.Geo = "{},{},5km".format(data['city']['lat'], data['city']['lng'])
  c.Time = 10

  socketio.emit('tweets', { 'message': 'Processing...', 'data': [] })
  threading.Thread(target=launch_query, args=(c,), daemon=True).start()
