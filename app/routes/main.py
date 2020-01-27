import json
from flask import render_template, session, Blueprint, redirect

main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

@main_bp.route('/')
def index():
  return render_template(
    'index.html',
    title = "Citizens sentiment analysis through their tweets",
    text = session.get('text') if session.get('text') else '',
  )

