import json
from flask_cors import cross_origin
from flask import Blueprint, request, jsonify, session

from .. import app

users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/users/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
  print(request.args)
  content = request.json
  if 'email' not in content or 'password' not in content:
    return jsonify({ 'error': 'Email and password are required' }), 400

  if content['email'] != 'test@test.com' or content['password'] != '12345678':
    return jsonify({ 'error': 'User not found' }), 404

  # User id from db
  session['user'] = 1
  return jsonify({ 'data': 'testing' })

@users_bp.route('/users/logout', methods=['POST'])
@cross_origin(supports_credentials=True)
def logout():
  session.pop('user')
  return jsonify({}), 201
