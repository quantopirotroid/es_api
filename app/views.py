from flask import jsonify
from flask import request, make_response
from app import app
from config import API_AUTH_TOKEN

from app.models.elastic import Data_validator, ES_handler

err = Data_validator()
esh = ES_handler()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': '404',
                                  'reason': 'Not found'}), 404)


@app.errorhandler(405)
def not_allowed_method(error):
    return make_response(jsonify({'error': '405',
                                  'reason': 'Method not allowed'}), 405)


@app.route('/')
def home():
    return 'Hello world'


@app.route('/api/add', methods=['POST'])
def add_element():
    header = request.headers.get('X-DB-api-auth-token')
    if header != API_AUTH_TOKEN:
        return make_response(jsonify({'error': 'Access denied!'}), 401)
    resp = esh.add_data(err, request.json)
    return jsonify(resp)


@app.route('/api/get', methods=['POST'])
def get_element():
    header = request.headers.get('X-DB-api-auth-token')
    if header != API_AUTH_TOKEN:
        return make_response(jsonify({'error': 'Access denied!'}), 401)
    resp = esh.get_from_id(err, request.json)
    return jsonify(resp)


@app.route('/api/search', methods=['POST'])
def search_element():
    header = request.headers.get('X-DB-api-auth-token')
    if header != API_AUTH_TOKEN:
        return make_response(jsonify({'error': 'Access denied!'}), 401)
    resp = esh.search(err, request.json)
    return jsonify(resp)
