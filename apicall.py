from flask import Flask, jsonify, request 

app = Flask(__name__)

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
    