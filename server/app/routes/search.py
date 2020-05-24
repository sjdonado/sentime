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

from flask_sqlalchemy import SQLAlchemy

from .. import socketio, app, db
from ..services import sentiment_classifier
from ..models import Search, Result

num_threads = 5
num_days = 1
cities_path = os.path.join(app.static_folder, 'data', 'colombia_departments_capitals_locations.json')

with open(cities_path) as f:
  cities = json.load(f)

# Blueprint Configuration
search_bp = Blueprint('search_bp', __name__,
                      template_folder='templates',
                      static_folder='static')

def save_results(city, lat, lng, scores, search_id):
  with app.app_context():
    result = Result()
    result.search_id = search_id
    result.city = city
    result.lat = lat
    result.lng = lng
    result.pos_score = len([score == True for score in scores])
    result.neg_score = len(scores) - result.pos_score
    result.total = len(scores)
    db.session.add(result)
    db.session.commit()

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

def launch_query(q, nlp, query, search_id):
  while True:
    city = q.get()
    print(city['formatted_address'], flush=True)

    c = twint.Config()
    c.Search = query
    c.Since = (date.today() - timedelta(days=num_days)).strftime('%Y-%m-%d %H:%M:%S')
    c.Limit = 80
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
      scores = sentiment_classifier.get_scores(nlp, tweets)

      city_name = city['formatted_address']
      lat = city['geometry']['location']['lat']
      lng = city['geometry']['location']['lng']

      save_results(city_name, lat, lng, scores, search_id)
      socketio.emit('tweets', {
        'status': 'processing',
        'data': {
          'city': city_name,
          'lat': lat,
          'lng': lng,
          'total': len(tweets),
          'scores': scores
        }
      })
      print("{} DONE!".format(city_name), flush=True)

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

    search = Search()
    search.user_id = session['user']
    search.query = session['query']
    db.session.add(search)
    db.session.commit()

    nlp = sentiment_classifier.init_nlp()

    for _ in range(num_threads):
      Thread(target=launch_query, args=(q, nlp, query, search.id), daemon=True).start()

    for city in cities:
      q.put(city)

    q.join()

    session['task_in_process'] = False
    socketio.emit('tweets', { 'status': 'finished' })
  else:
    socketio.emit('tweets', { 'status': 'task_in_progress' })
