import json
from flask import render_template, session, Blueprint, redirect

main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

@main_bp.route('/')
def index():
  print("INDEX tweets => {}".format(session.get('tweets')))
  return render_template(
    'index.html',
    title = "Citizens sentiment analysis through their tweets",
    tweets = json.dumps(session.get('tweets')) if session.get('tweets') else [],
    text = session.get('text'),
  )

