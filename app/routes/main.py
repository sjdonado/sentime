import os
import json
from flask import render_template, session, Blueprint, redirect

from .. import app

cities_path =  os.path.join(app.static_folder, 'data', 'co.json')

main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

@main_bp.route('/')
def index():
  return render_template(
    'index.html',
    title = "Citizens sentiment analysis through their tweets",
    cities = json.load(open(cities_path)),
    city = session.get('city') if session.get('city') else '',
    text = session.get('text') if session.get('text') else '',
  )

