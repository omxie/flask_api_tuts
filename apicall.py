from flask import Flask, jsonify 

app = Flask(__name__)

@app.route('/apicall')
def apicall():
    return jsonify(message='hello API')


@app.route('/not_found')
def not_found():
    return jsonify(message='Resource Not found'), 404