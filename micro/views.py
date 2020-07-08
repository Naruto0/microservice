from flask import request, abort, make_response, jsonify, render_template

from micro import app
from micro.offers_api import get_offers
from micro.api import add_product, update_product, delete_product, register_client,check_uuid

ROUTE = '/micro/api/v1'
"""Routes for local API"""


def authorized_access(response):
    return check_uuid(response.headers.get('Bearer'))


def process_response(res):
    status_code = res['status_code']
    del res['status_code']
    return make_response(jsonify(res), status_code)


@app.route(f'{ROUTE}/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route(f'{ROUTE}/auth', methods=['POST'])
def get_authorization():
    r = register_client()
    return process_response(r)


@app.route(f'{ROUTE}/<id>/offers')
def ll(id):
    return '%s' % get_offers(id).json()


@app.route(f'{ROUTE}/add', methods=['POST'])
def add():
    access, response = authorized_access(request)
    if access:
        data = request.get_json()
        r = add_product(data)
    else:
        r = response
    return process_response(r)


@app.route(f'{ROUTE}/update', methods=['PUT'])
def update():
    access, response = authorized_access(request)
    if access:
        data = request.get_json()
        r = update_product(data)
    else:
        r = response
    return process_response(r)


@app.route(f'{ROUTE}/<id>/delete', methods=['DELETE'])
def delete(id):
    access, response = authorized_access(request)
    if access:
        r = delete_product(id)
    else:
        r = response
    return process_response(r)
