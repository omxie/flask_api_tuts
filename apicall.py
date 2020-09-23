from flask import Flask, jsonify, request 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'planets.db')

db=SQLAlchemy(app)



@app.route('/apicall')
def apicall():
    return jsonify(message='hello API')


@app.route('/not_found')
def not_found():
    return jsonify(message='Resource Not found'), 404


@app.route('/parameters/<string:name>/<int:age>')
def parameters(name: str, age: int):
    if age < 18: 
        return jsonify(message='You are not old enough to visit this page'), 401
    else:
        return jsonify(message='Welcome '+name+', you are old enough to visit the website!')
    

class User(db.Model):
    __tablename__='users'
    id = Column(Integer, primary_key=True)
    fname = Column(String)
    lname = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

class Planet(db.Model):
    __tablename__ = 'planets'
    planet_id = Column(Integer, primary_key=True)
    pname = Column(String)
    ptype = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)