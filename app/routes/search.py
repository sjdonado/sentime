import os
import json

import twint
import asyncio

from queue import Queue
from threading import Thread

from datetime import date
from datetime import timedelta

from flask import session, Blueprint

from .. import socketio, app

num_threads = 5
num_days = 1
cities_path = os.path.join(app.static_folder, 'data', 'colombia_departments_capitals_locations.json')

with open(cities_path) as f:
  cities = json.load(f)

# Blueprint Configuration
search_bp = Blueprint('search_bp', __name__,
                      template_folder='templates',
                      static_folder='static')

def launch_query(q, text):
  while True:
    city = q.get()
    print(city['formatted_address'], flush=True)

    c = twint.Config()
    c.Search = text
    c.Since = (date.today() - timedelta(days=num_days)).strftime('%Y-%m-%d')
    c.Store_object = True
    c.Location = True
    c.Hide_output = True
    c.Show_hashtags = False
    # TODO: Fit radio based on city boundaries
    c.Geo = "{},{},5km".format(
      city['geometry']['location']['lat'],
      city['geometry']['location']['lng']
    )
    print('event loop => ', asyncio.get_event_loop(), flush=True)
    twint.run.Search(c)
    tweets = [t.__dict__ for t in twint.output.tweets_list]
    socketio.emit('tweets', {
      'status': 'processing',
      'data': {
        'city': city,
        'tweets': tweets
      }
    })

    q.task_done()

@socketio.on('search')
def search(message):
  data = json.loads(message)
  text = data['text']
  session['text'] = text

  q = Queue(maxsize=0)
  asyncio.set_event_loop(asyncio.new_event_loop())

  socketio.emit('tweets', { 'status': 'started' })

  for _ in range(num_threads):
    Thread(target=launch_query, args=(q, text), daemon=True).start()

  for city in cities:
    q.put(city)

  q.join()

  socketio.emit('tweets', { 'status': 'finished' })

