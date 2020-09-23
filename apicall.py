from flask import Flask, jsonify, request 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'planets.db')

db=SQLAlchemy(app)
ma=Marshmallow(app)


@app.cli.command('db_create')
def db_create():
    db.create_all()

@app.cli.command('db_drop')
def db_drop():
    db.drop_all()

@app.cli.command('db_seed')
def db_seed():
    mercury=Planet(pname='mercury',
                    ptype='plan',
                    home_star='sol',
                    mass=3.222545,
                    radius=3211,
                    distance=5664)

    venus=Planet(pname='venus',
                    ptype='plan',
                    home_star='sol',
                    mass=3.222545,
                    radius=3211,
                    distance=5664)

    db.session.add(mercury)
    db.session.add(venus)

    test_user=User(fname='Om',
                    lname='Panchal',
                    email='omx@test.com',
                    password='123456')
    
    db.session.add(test_user)
    db.session.commit()


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
    
@app.route('/planets', methods=['GET'])
def planets():
    planets_list=Planet.query.all()
    result = planets_schema.dump(planets_list)
    return jsonify(result)

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

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'fname', 'lname', 'email', 'password')

class PlanetSchema(ma.Schema):
    class Meta:
        fields = ('planet_id','pname', 'ptype', 'home_star', 'mass', 'radius', 'distance')


planet_schema=PlanetSchema()
planets_schema=PlanetSchema(many=True)

user_schema=UserSchema()
users_schema=UserSchema(many=True)

