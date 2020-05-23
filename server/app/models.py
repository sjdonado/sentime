import os
from datetime import datetime
from flask import Flask, abort, request, jsonify, url_for
from . import db, create_app
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    # Define the columns of the users table, starting with the primary key
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    company = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # def set_password(self, password):
    #     self.password = generate_password_hash(password)

    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password) 
    

class Search(db.Model):
    __tablename__ = 'searches'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    query = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_JSON(self):
        res = {}
        for attr in ('id','user_id','query'):
            res[attr] = getattr(self, attr)
        res['results'] = self.get_results()
        return res
    
    def get_results(self):
        res = []
        results = db.session.query(Result).filter_by(search_id=getattr(self, 'id'))
        for result in results:
            res.append(result.to_JSON())
        return res
        

class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    search_id = db.Column(db.Integer, db.ForeignKey('searches.id'), nullable=False)
    search = db.relationship(Search)
    city = db.Column(db.String, nullable=False)
    pos_score = db.Column(db.Integer, nullable=False)
    neg_score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_JSON(self):
        res = {}
        for attr in ('id','city','pos_score','neg_score'):
            res[attr] = getattr(self, attr)
        return res