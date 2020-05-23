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
  print(request.args)
  content = request.json
  if 'email' not in content or 'password' not in content:
    return jsonify({ 'error': 'Email and password are required' }), 400

  # if content['email'] != 'test@test.com' or content['password'] != '12345678':
  #   return jsonify({ 'error': 'Usuario no encontrado' }), 404

  user = User.query.filter_by(email=content['email']).first()
  if user:
    if (content['email'] != user.email) or (not check_password_hash(user.password, content['password'])):
      return jsonify({ 'error': 'Usuario o contraseña incorrectas' }), 404
    else:
      session['user'] = user.id
      #session['user'] = 1
      return jsonify({ 'email': content['email'] })
  else:
    return jsonify({ 'error': 'Usuario no encontrado' }), 404


  # User id from db
  #session['user'] = 1
  #return jsonify({ 'email': content['email'] })

@users_bp.route('/users/logout', methods=['POST'])
@cross_origin(supports_credentials=True)
def logout():
  session.pop('user')
  return jsonify({}), 201


@users_bp.route('/users/u_history', methods=['POST'])
@cross_origin(supports_credentials=True)
def u_history():
  response = []
  searches = db.session.query(Search).filter_by(user_id=session['user'])
  for search in searches:
    response.append(search.to_JSON())
    #results = db.session.query(Result).filter(Result.search_id.in_(search.as_scalar()))
  #print(response, flush=True)
  print(response, flush=True)
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
      print('user registered', flush=True)
      return jsonify({'message':'User registration was succesful','email': user.email})
    
    except Exception as e:
                    response = {
                        'message': str(e)
                        }
                    return response


