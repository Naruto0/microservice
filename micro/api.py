from micro.models import Product, Offer
from micro.database import db
from micro.offers_api import *

from micro import app


def add_product(payload):
    try:
        p = Product(payload['name'], payload['description'])
    except Exception as e:
        return e
    db.session.add(p)
    app.logger(p.id)
    register_item(p.id, p.name, p.description)


def update_product(payload):
    pass


def delete_product(id):
    pass