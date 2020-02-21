import csv
import json
from flask import render_template, session, Blueprint, redirect

from .. import app

main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

@main_bp.route('/')
def index():
  return render_template(
    'index.html',
    title = "Citizens sentiment analysis through their tweets",
    text = session.get('text') if session.get('text') else '',
    access_token = 'pk.eyJ1IjoicGFzdG9yaXpvaiIsImEiOiJjazV6cDh2YnAwMjBhM2ptbWhveXpuOGw5In0.97o-ntf0qtgJoOmg9l3ESA',
  )

