from micro.database import db
from datetime import datetime
"""Microservice models definition"""


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(128), unique=True, nullable=False)
    offers = db.relationship("Offer", backref='product')


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    items_in_stock = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    timestamp = db.Column(db.DateTime)


class Client(db.Model):
    id = db.Column(db.String(32), primary_key=True, nullable=False)
