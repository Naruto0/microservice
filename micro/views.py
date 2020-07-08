from flask import request, abort, make_response, jsonify

from micro import app
from micro.offers_api import get_offers
from micro.api import add_product, update_product

ROUTE = '/micro/api/v1'


@app.route(f'{ROUTE}/')
def home():
    return 'Hello app'


@app.route(f'{ROUTE}/<id>/offers')
def ll(id):
    return '%s' % get_offers(id).json()


@app.route(f'{ROUTE}/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        data = request.get_json()
        r = add_product(data)
        status_code = r['status_code']
        del r['status_code']
        return make_response(jsonify(r), status_code)


@app.route(f'{ROUTE}/update', methods=['PUT'])
def update():
    data = request.get_json()
    r = update_product(data)
    status_code = r['status_code']
    del r['status_code']
    return make_response(jsonify(r), status_code)


@app.route('/<id>/delete', methods=['DELETE'])
def delete():
    pass
