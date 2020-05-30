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

from flask import session, Blueprint, jsonify

from flask_sqlalchemy import SQLAlchemy

from .. import socketio, app, db, logger
from ..services import sentiment_classifier
from ..models import Search, Result

NUM_THREADS = 6
CITIES_PATH = os.path.join(app.static_folder, 'data', 'colombia_departments_capitals_locations.json')

with open(CITIES_PATH) as f:
  cities = json.load(f)

search_bp = Blueprint('search_bp', __name__)

def save_results(city, lat, lng, scores, search_id):
  with app.app_context():
    result = Result()
    result.search_id = search_id
    result.city = city
    result.lat = lat
    result.lng = lng
    result.positive = scores['positive']
    result.negative = scores['negative']
    result.neutral = scores['neutral']
    result.total = scores['positive'] + scores['negative'] + scores['neutral']
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

def launch_query(q, query, hours, user_id, search_id):
  while True:
    city = q.get()
    print("Searching... {}".format(city['formatted_address']))

    c = twint.Config()
    c.Search = query
    c.Since = (date.today() - timedelta(hours==hours)).strftime('%Y-%m-%d %H:%M:%S')
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
      scores = sentiment_classifier.get_scores(tweets)

      city_name = city['formatted_address']
      lat = city['geometry']['location']['lat']
      lng = city['geometry']['location']['lng']

      print("results: {}".format(scores))
      save_results(city_name, lat, lng, scores, search_id)
      socketio.emit('tweets', {
        'id': user_id, 
        'status': 'processing',
        'data': {
          'city': city_name,
          'lat': lat,
          'lng': lng,
          'total': len(tweets),
          'scores': scores
        }
      })
      # with app.test_request_context():
      #   session['task_in_process'] += 1
      #   if session['task_in_process'] == 32:
      #     socketio.emit('tweets', { 'status': 'finished' })
      print(tweets, scores, flush=True)
      q.task_done()

    twint.run.Search(c, callback=callback)

# def threaded_func(q, query, hours, user_id, search_id):
#   el = asyncio.new_event_loop()
#   el.run_until_complete(launch_query(q, query, hours, user_id, search_id))

@socketio.on('search')
def search(message):
  data = json.loads(message)
  query = data['query']
  hours = data['hours']

  logger.info("Search: {}, hours: {}".format(query, hours))

  try:
    if 'task_in_process' not in session:
      session['task_in_process'] = 0

    if session['task_in_process'] == 0:
      session['task_in_process'] = 1
      q = Queue(maxsize=0)

      socketio.emit('tweets', { 'status': 'started' })

      search = Search()
      search.user_id = session['user_id']
      search.query = query
      db.session.add(search)
      db.session.commit()

      for _ in range(NUM_THREADS):
        Thread(target=launch_query, args=(q, query, hours, session['user_id'], search.id), daemon=True).start()

      for city in cities:
        q.put(city)

      q.join()    
    else:
      socketio.emit('tweets', { 'status': 'task_in_progress' })
  except Exception as e:
    session['task_in_process'] = 0
    socketio.emit('tweets', { 'status': 'finished', 'message': str(e) })

@search_bp.route('/search/status', methods=['GET'])
def model_status():
  health = sentiment_classifier.get_health()
  return jsonify({ 'status': health })