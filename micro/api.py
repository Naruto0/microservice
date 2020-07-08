from micro.models import Product, Offer
from micro.database import db
from micro.offers_api import *


def add_product(payload):
    try:
        p = Product(**payload)
    except Exception as e:
        db.session.rollback()
        return {'status_code': 400, 'msg': str(e)}
    db.session.add(p)
    try:
        db.session.commit()
    except Exception as e:
        return {'status_code': 400, 'msg': str(e)}
    r = register_item(p.id, p.name, p.description)
    if r.status_code != 201:
        db.session.delete(p)
        db.session.commit()
    payload = r.json()
    payload['status_code'] = r.status_code
    return payload


def update_product(payload):
    p = Product.query.get(payload['id'])
    if p is not None:
        p.name = payload['name']
        p.description = payload['description']
        db.session.commit()
        return {'status_code': 201, 'modified': {'id': p.id, 'name': p.name, 'description': p.description}}
    else:
        return {'status_code': 404, 'msg': f'Product with id {payload["id"]} does not exist.'}


def delete_product(id):
    try:
        q = Product.query.get(id)
        db.session.delete(q)
        db.session.commit()
    except Exception as e:
        return {'code': 'ERROR', 'msg': e}