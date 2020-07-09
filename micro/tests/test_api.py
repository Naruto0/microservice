import pytest
import json
import responses

from micro import app
from micro.database import db, init_db
from micro.views import ROUTE
from micro.models import Product, Client


@pytest.fixture
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client


@pytest.fixture
def auth():
    c = Client.query.all()[0]
    yield c.id


def test_auth_call(client):
    """Test `/auth` functionality"""
    response = client.post(f'{ROUTE}/auth')
    token = response.json['Bearer']
    c = Client.query.all()[0]
    assert c.id == token


@responses.activate
def test_object_creation(client, auth):
    """Create product and hand it over to remote API"""
    payload = {"name": "SOLO", "description": "Bezpečnostní zápalky."}
    responses.add(
        responses.POST,
        'https://applifting-python-excercise-ms.herokuapp.com/api/v1/products/register',
        status=201,
        body=json.dumps({"id": 1})
    )
    r = client.post(f'{ROUTE}/add', headers={'Bearer': auth}, json=payload)
    q = Product.query.get(1)
    assert q.id == r.json['id']  # object in database corresponds to returned


def test_unauthorized_creation(client):
    """Attempt to create Product without authorization code"""
    payload = {"name": "Pistole W0D4", "description": "Hračková pistole na vodu."}
    r = client.post(f'{ROUTE}/add', json=payload)
    assert r.status_code == 401


def test_duplicate_creation(client, auth):
    """Attempt to create Product with duplicate name/description"""
    payload = {"name": "SOLO", "description": "Bezpečnostní zápalky."}
    r = client.post(f'{ROUTE}/add', headers={'Bearer': auth}, json=payload)
    assert r.status_code == 400


def test_update_product(client, auth):
    """Product `q` shall have different name/description from `q2`."""
    q = Product.query.get(1)
    old_name = q.name
    old_description = q.description
    payload = {"id": 1, "name": "Baťa cvičky", "description": "Retro sportovní boty světoznáme značky."}
    r = client.put(f'{ROUTE}/update', headers={'Bearer': auth}, json=payload)
    assert r.status_code == 201
    q2 = Product.query.get(1)
    assert old_name != q2.name or old_description != q2.description


def test_unauthorized_update(client):
    """Attempt to create Product without authorization code."""
    payload = {"id": 1, "name": "Pruhy Zeebra", "description": "Nalepovací maškarní zebra-pruhy."}
    r = client.put(f'{ROUTE}/update', json=payload)
    assert r.status_code == 401


def test_edit_nonexistent(client, auth):
    """Fail to update non-existent product."""
    payload = {"id": 4, "name": "Ilumix", "description": "Stylova stolni lampa."}
    r = client.put(f'{ROUTE}/update', headers={'Bearer': auth}, json=payload)
    assert r.status_code == 404


@responses.activate
def test_delete_product(client, auth):
    """Delete item"""
    payload = {"name": "Žabka", "description": "Síťovaná taška."}
    responses.add(
        responses.POST,
        'https://applifting-python-excercise-ms.herokuapp.com/api/v1/products/register',
        status=201,
        body=json.dumps({"id": 2})
    )
    client.post(f'{ROUTE}/add', headers={'Bearer': auth}, json=payload)
    q = db.session.query(Product).filter(Product.name == "Žabka")
    id = q[0].id
    res = client.delete(f'{ROUTE}/{id}/delete', headers={'Bearer': auth})
    assert res.status_code == 200  # deletion performed in database
    i = Product.query.get(id)
    assert i is None  # item does no longer exist in database


def test_delete_unauthorized(client):
    """Fail to delete without auth"""
    p = Product.query.one()
    res = client.delete(f'{ROUTE}/{p.id}/delete')
    assert res.status_code == 401


def test_delete_nonexistent(client, auth):
    r = client.delete(f'{ROUTE}/1000/delete', headers={'Bearer': auth})
    assert r.status_code == 404
