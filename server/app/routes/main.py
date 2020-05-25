from flask import Blueprint, jsonify

from .. import app

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def index():
  return jsonify({ 'status': 'ok' })
