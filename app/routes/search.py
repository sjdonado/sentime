import os
import json

import twint
import asyncio
import threading

from datetime import date
from datetime import timedelta

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

  tweets_by_cities = []
  last_len = 0

  for idx, city in enumerate(cities):
    # TODO: Fit radio based on city boundaries
    c.Geo = "{},{},5km".format(
      city['geometry']['location']['lat'],
      city['geometry']['location']['lng']
    )
    twint.run.Search(c)
    tweets = [t.__dict__ for t in twint.output.tweets_list[last_len:]]
    last_len = len(tweets)
    socketio.emit('tweets', {
      'status': 'processing',
      'progress': (idx + 1) / 32,
      'data': {
        'city': city,
        'results': last_len,
        'tweets': map(lambda t: t['tweet'], tweets)
      }
    })
    tweets_by_cities.append({
      'city': city,
      'tweets': map(lambda t: t['tweet'], tweets)
    })

  socketio.emit('tweets', { 'status': 'finished', 'data': tweets_by_cities })

@socketio.on('search')
def search(message):
  data = json.loads(message)
  session['text'] = data['text']
  c = twint.Config()
  c.Search = data['text']
  c.Since = date.today() - timedelta(days=7)
  c.Store_object = True
  c.Location = True
  c.Hide_output = True
  c.Show_hashtags = False

  socketio.emit('tweets', { 'status': 'started', 'data': [] })
  threading.Thread(target=launch_query, args=(c,), daemon=True).start()
