from flask import Flask, jsonify, request 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mail import Mail, Message
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'planets.db')
app.config['JWT_SECRET_KEY']='super_secret_key'
app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
#app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
#app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']


db=SQLAlchemy(app)
ma=Marshmallow(app)
jwt=JWTManager(app)
mail = Mail(app)

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

@app.route('/register',methods=['POST'])
def register():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message='That email exists!'), 409
    else:
        first_name = request.form['fname']
        last_name= request.form['lname']
        password = request.form['password']
        user = User(fname=first_name, lname=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message='created successfully!'), 201

@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = User.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity = email)
        return jsonify(message='login successfull', access_token=access_token)
    else:
        return jsonify(message='invalid email'), 401


@app.route('/forgotpass/<string:email>', methods=['GET'])
def forgotpass(email:str):
    #checks whether user exits and stores the results in variable 'user'
    user = User.query.filter_by(email=email).first()
    if user:
        msg = Message("your planetary api password is"+user.password, 
        sender = "admin@wwb.com", 
        recipients=[email])
        mail.send(msg)
        return jsonify(message = "Password sent to "+email)
    else:
        return jsonify(message = "does not exists")

#gets the planet name for id of the planet
@app.route('/planet_details/<int:planet_id>', methods=['GET'])
def planet_details(planet_id : int):
    test = Planet.query.filter_by(planet_id=planet_id).first()
    if test:
        result = planet_schema.dump(test)
        return jsonify(result)
    else:
        return jsonify(message='planet for the given id does not exists'), 404

@app.route('/add_planet', methods = ['POST'])
@jwt_required
def add_planet():
    planet_name=request.form['pname']
    test = Planet.query.filter_by(pname=planet_name).first()
    if test:
        return jsonify('Planet already exists!')
    else:
        planet_name=request.form['pname']
        ptype = request.form['ptype']
        home_star = request.form['hstar']
        mass = request.form['mass']
        radius = request.form['radius']
        distance = request.form['distance']

        new_planet = Planet(pname=planet_name,
        ptype = ptype,
        home_star = home_star,
        mass=mass,
        radius=radius,
        distance= distance)
    
        db.session.add(new_planet)
        db.session.commit()
        return jsonify(message="You added a planet to the database!")


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

