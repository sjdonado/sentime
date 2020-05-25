import json
from flask_cors import cross_origin
from flask import Blueprint, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from .. import app, db
from ..models import User, Result, Search

users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/users/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
  content = request.json
  if 'email' not in content or 'password' not in content:
    return jsonify({ 'error': 'Email and password are required' }), 400

  user = User.query.filter_by(email=content['email']).first()
  if user:
    if (content['email'] != user.email) or (not check_password_hash(user.password, content['password'])):
      return jsonify({ 'error': 'Usuario o contraseña incorrectas' }), 404
    else:
      session['user_id'] = user.id
      return jsonify(user.to_JSON())
  else:
    return jsonify({ 'error': 'Usuario no encontrado' }), 404

@users_bp.route('/users/logout', methods=['POST'])
@cross_origin(supports_credentials=True)
def logout():
  session.pop('user_id')
  return jsonify({}), 201

@users_bp.route('/users/history', methods=['POST'])
@cross_origin(supports_credentials=True)
def history():
  response = []
  searches = db.session.query(Search).filter_by(user_id=session['user_id'])
  for search in searches:
    response.append(search.to_JSON())

  return(jsonify(response))
  
@users_bp.route('/users/register', methods=['POST'])
@cross_origin(supports_credentials=True)
def register():
  content = request.json
  user = User.query.filter_by(email=content['email']).first()
  
  if user == None:
    try:
      email = content['email']
      password = content['password']
      company = content['company']

      user = User()
      user.email = email
      user.password = generate_password_hash(password)
      user.company = company
      
      db.session.add(user)
      db.session.commit()

      return jsonify(user.to_JSON())
    except Exception as e:
      return jsonify({ 'message': str(e) })

  return jsonify({ 'error': 'Este correo ya se encuentra registrado' })


