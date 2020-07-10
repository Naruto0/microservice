import pytest
import json
import responses
from datetime import datetime as dt

from micro import app
from micro.database import db, init_db
from micro.views import ROUTE
from micro.models import Product, Client, Offer


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
    """Fail to delete non-existent record"""
    r = client.delete(f'{ROUTE}/1000/delete', headers={'Bearer': auth})
    assert r.status_code == 404


def test_query_products(client, auth):
    """Query all registered and valid products"""
    r = client.get(f'{ROUTE}/products', headers={'Bearer': auth})
    assert r.status_code == 200


def test_get_product_details(client, auth):
    """Query product details"""
    date = dt(2020, 8, 2)
    o1_payload = {'id': 1, 'items_in_stock': 25, 'price': 152,
                  'timestamp': 'Sun, 02 Aug 2020 00:00:00 GMT',
                  'vendor_id': 16542
                  }
    o2_payload = {'id': 2, 'items_in_stock': 12, 'price': 200,
                  'timestamp': 'Sun, 02 Aug 2020 00:00:00 GMT',
                  'vendor_id': 17462
                  }
    o1 = Offer(
        vendor_id=16542, price=152, items_in_stock=25,
        product_id=1, timestamp=date
    )
    o2 = Offer(
        vendor_id=17462, price=200, items_in_stock=12,
        product_id=1, timestamp=date
    )
    db.session.add_all([o1, o2])
    db.session.commit()
    r = client.get(f'{ROUTE}/1/detail', headers={'Bearer': auth})
    assert r.status_code == 200
    offers = r.json['offers']
    assert o1_payload in offers
    assert o2_payload in offers
