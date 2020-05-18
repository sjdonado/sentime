from os import environ
import redis

class Config:
  # General Config
  SECRET_KEY = environ.get('SECRET_KEY')
  FLASK_ENV = environ.get('FLASK_ENV')
  CORS_HEADERS='Content-Type'

  # Flask-Session
  SESSION_TYPE = 'redis'
  SESSION_REDIS = redis.from_url(environ.get('REDIS_URL'))

  # Database Config
  #SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')