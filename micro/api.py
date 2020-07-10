from micro.models import Product, Client
from micro.database import db
from micro.offers_api import register_item
from uuid import uuid1

"""Local application layer package."""

UNAUTHORIZED = {
    "status_code": 401,
    "msg": "Unknown user, please use Bearer token"
}


def serialize_product(prod):
    return {
        "id": prod.id,
        "name": prod.name,
        "description": prod.description,
    }


def serialize_offer(of):
    return {
        "id": of.id,
        "vendor_id": of.vendor_id,
        "price": of.price,
        "items_in_stock": of.items_in_stock,
        "timestamp": of.timestamp,
    }


def check_uuid(token):
    """Checks if received `Bearer` is in database"""
    q = Client.query.get(token)
    if q is None:
        return False, {"status_code": 401, "msg": "Unauthorized acces"}
    return True, None


def register_client():
    """Simply generates and saves an ID responses it back"""
    c = Client(id=uuid1().hex)
    db.session.add(c)
    db.session.commit()
    return {"status_code": 201, "Bearer": c.id}


def add_product(payload):
    """Save product in database, on success hand it out to remote API"""
    try:
        p = Product(**payload)
    except Exception as e:
        db.session.rollback()
        return {"status_code": 400, "msg": str(e)}
    db.session.add(p)
    try:
        db.session.commit()
    except Exception as e:
        return {"status_code": 400, "msg": str(e)}
    r = register_item(p.id, p.name, p.description)
    if r.status_code != 201:
        db.session.delete(p)
        db.session.commit()
    payload = r.json()
    payload["status_code"] = r.status_code
    return payload


def update_product(payload):
    """Update product `name`/`description`"""
    p = Product.query.get(payload["id"])
    if p is None:
        return {
            "status_code": 404,
            "msg": f'Product with id {payload["id"]} does not exist.',
        }
    p.name = payload["name"]
    p.description = payload["description"]
    db.session.commit()
    return {
        "status_code": 201,
        "item": {"id": p.id, "name": p.name, "description": p.description},
    }


def delete_product(id):
    """Delete product from database"""
    q = Product.query.get(id)
    if q is None:
        return {
            "status_code": 404,
            "msg": f"Cannot delete product {id} that does not exist.",
        }
    db.session.delete(q)
    db.session.commit()
    return {
        "status_code": 200,
        "msg": f"Product id: {q.id} deleted.",
        "item": {"id": q.id, "name": q.name, "description": q.description},
    }


def query_products():
    q = Product.query.all()
    payload = []
    if q is None:
        return {"status_code": 404, "msg": "No product registred yet."}
    for product in q:
        item = serialize_product(product)
        payload.append(item)
    return {"status_code": 200, "products": payload}


def query_detail(product_id):
    p = Product.query.get(product_id)
    if p is None:
        return {
            "status_code": 404,
            "msg": f"Product with id {product_id} does not exist.",
        }
    children = []
    for child in p.offers:
        children.append(serialize_offer(child))
    return {
        "status_code": 200,
        "product": serialize_product(p),
        "offers": children
    }
