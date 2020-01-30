import twint
import asyncio
import threading
import json

from flask import redirect, request, session, Blueprint, copy_current_request_context

from .. import socketio

# Blueprint Configuration
search_bp = Blueprint('search_bp', __name__,
                      template_folder='templates',
                      static_folder='static')

def launch_query(c):
  asyncio.set_event_loop(asyncio.new_event_loop())
  twint.run.Search(c)

  tweets = [t.__dict__ for t in twint.output.tweets_list]
  print("DATA => {}".format(tweets), flush=True)
  socketio.emit('tweets', { 'data': tweets })

@socketio.on('search')
def search(message):
  data = json.loads(message)

  session['text'] = data['text']
  c = twint.Config()
  c.Search = data['text']
  c.Store_object = True
  c.Near = data['city']
  c.Limit = 100

  socketio.emit('tweets', { 'data': 'processing...' })
  threading.Thread(target=launch_query, args=(c,), daemon=True).start()
