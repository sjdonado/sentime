import twint
import asyncio
import threading

from flask import redirect, request, session, Blueprint, copy_current_request_context

from .. import app

# Blueprint Configuration
search_bp = Blueprint('search_bp', __name__,
                      template_folder='templates',
                      static_folder='static')

def launch_query(c):
  with app.test_request_context():
    from flask import session

    asyncio.set_event_loop(asyncio.new_event_loop())
    twint.run.Search(c)

    tweets = twint.output.tweets_list
    session['tweets'] = tweets
    print("launch query => {}".format(session.get('tweets')), flush=True)

@search_bp.route('/search', methods=['POST'])
def search():
  session['text'] = request.values.get('text')
  c = twint.Config()
  c.Search = session.get('text')
  c.Store_object = True

  threading.Thread(target=launch_query, args=(c,)).start()
  print('thread start...', flush=True)
  return redirect('/')
