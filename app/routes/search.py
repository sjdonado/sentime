import os
import json

import twint
import asyncio
import threading

from flask import session, Blueprint

from .. import socketio, app

cities_path = os.path.join(app.static_folder, 'data', 'colombia_departments_capitals_locations.json')

with open(cities_path) as f:
  cities = json.load(f)

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
  print(message)
  data = json.loads(message)
  session['text'] = data['text']
  c = twint.Config()
  c.Search = data['text']
  c.Store_object = True
  c.Location = True
  c.Limit = 100

  # TODO: Add each city thread to a Queue

  c.Geo = "{},{},5km".format(cities[0]['geometry']['location']['lat'], cities[0]['geometry']['location']['lng'])

  # for city in cities:
  #   c.Geo = "{},{},5km".format(city['geometry']['location']['lat'], city['geometry']['location']['lng'])
  socketio.emit('tweets', { 'message': 'Processing...', 'data': [] })
  threading.Thread(target=launch_query, args=(c,), daemon=True).start()
