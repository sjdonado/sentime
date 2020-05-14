import os
from flask import Flask, abort, request, jsonify, url_for
from . import db, create_app
from flask import current_app


class User(db.Model):
    """This class defines the users table """

    __tablename__ = 'users'

    # Define the columns of the users table, starting with the primary key
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    company = db.Column(db.String(256), nullable=False)

