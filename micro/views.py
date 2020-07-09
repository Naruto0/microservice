from flask import request, make_response, jsonify, render_template

from micro import app
from micro.api import add_product, update_product, delete_product, register_client, check_uuid

ROUTE = '/micro/api/v1'
"""Routes for local API"""


def authorized_access(response):
    """Check if access is authorized"""
    return check_uuid(response.headers.get('Bearer'))


def process_response(res):
    """Helper function to refactor code"""
    status_code = res['status_code']
    del res['status_code']
    return make_response(jsonify(res), status_code)


@app.route(f'{ROUTE}/', methods=['GET'])
def home():
    """Home page"""
    return render_template('index.html')


@app.route(f'{ROUTE}/auth', methods=['POST'])
def get_authorization():
    """API endpoint to get authentication code"""
    r = register_client()
    return process_response(r)


@app.route(f'{ROUTE}/add', methods=['POST'])
def add():
    """API endpoint to add Product"""
    access, response = authorized_access(request)
    if access:
        data = request.get_json()
        r = add_product(data)
    else:
        r = response
    return process_response(r)


@app.route(f'{ROUTE}/update', methods=['PUT'])
def update():
    """API endpoint to update Product"""
    access, response = authorized_access(request)
    if access:
        data = request.get_json()
        r = update_product(data)
    else:
        r = response
    return process_response(r)


@app.route(f'{ROUTE}/<id>/delete', methods=['DELETE'])
def delete(id):
    """API endpoint to delete Product"""
    access, response = authorized_access(request)
    if access:
        r = delete_product(id)
    else:
        r = response
    return process_response(r)
