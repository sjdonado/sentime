import os
import json
import math

import twint
import asyncio
from geopy.distance import distance

from queue import Queue
from threading import Thread

from datetime import date
from datetime import timedelta

from flask import session, Blueprint

from .. import socketio, app
from ..services import forecast

num_threads = 5
num_days = 1
cities_path = os.path.join(app.static_folder, 'data', 'colombia_departments_capitals_locations.json')

with open(cities_path) as f:
  cities = json.load(f)

# Blueprint Configuration
search_bp = Blueprint('search_bp', __name__,
                      template_folder='templates',
                      static_folder='static')

def launch_query(q, query):
  while True:
    city = q.get()
    print(city['formatted_address'], flush=True)

    c = twint.Config()
    c.Search = query
    c.Since = (date.today() - timedelta(days=num_days)).strftime('%Y-%m-%d %H:%M:%S')
    c.Limit = 1
    c.Filter_retweets = True
    c.Store_object = True
    c.Location = True
    c.Hide_output = True
    c.Show_hashtags = False
    c.Lang = 'es'
    c.Pandas = True
    geo =  get_geo(city)
    c.Geo = geo

    def callback(args):
      total_tweets = [t.__dict__ for t in twint.output.tweets_list]
      tweets = list(filter(lambda t: t['geo'] == geo, total_tweets))
      tweets = list(map(lambda t: t['tweet'], tweets))
      score = forecast.get_score(tweets)
      socketio.emit('tweets', {
        'status': 'processing',
        'data': {
          'city': city,
          'tweets': tweets,
          'score': score
        }
      })

      print("{} DONE!".format(city['formatted_address']), flush=True)
      q.task_done()

    twint.run.Search(c, callback=callback)

@socketio.on('search')
def search(message):
  data = json.loads(message)
  query = data['query']
  session['query'] = query

  if 'task_in_process' not in session:
    session['task_in_process'] = False

  if session['task_in_process'] == False:
    session['task_in_process'] = True
    q = Queue(maxsize=0)

    socketio.emit('tweets', { 'status': 'started' })

    for _ in range(num_threads):
      Thread(target=launch_query, args=(q, query), daemon=True).start()

    for city in cities:
      q.put(city)

    q.join()

    session['task_in_process'] = False
    socketio.emit('tweets', { 'status': 'finished' })
  else:
    socketio.emit('tweets', { 'status': 'Wait for task in process' })

def get_geo(city):
  def midpoint(x1, y1, x2, y2):
    lat1 = math.radians(x1)
    lon1 = math.radians(x2)
    lat2 = math.radians(y1)
    lon2 = math.radians(y2)

    bx = math.cos(lat2) * math.cos(lon2 - lon1)
    by = math.cos(lat2) * math.sin(lon2 - lon1)
    lat3 = math.atan2(math.sin(lat1) + math.sin(lat2), \
            math.sqrt((math.cos(lat1) + bx) * (math.cos(lat1) \
            + bx) + by**2))
    lon3 = lon1 + math.atan2(by, math.cos(lat1) + bx)

    return [round(math.degrees(lat3), 2), round(math.degrees(lon3), 2)]

  northeastBound = (city['geometry']['bounds']['northeast']['lat'],city['geometry']['bounds']['northeast']['lng'])
  southwestBound = (city['geometry']['bounds']['southwest']['lat'],city['geometry']['bounds']['southwest']['lng'])
  latCenter, lngCenter = midpoint(northeastBound[0],southwestBound[0],northeastBound[1],southwestBound[1])
  radius = ((math.sin(45)*(distance(northeastBound,southwestBound).km / 2)))/math.sin(45)

  geo = "{},{},{}km".format(
    latCenter,
    lngCenter,
    radius
  )
  return geo
