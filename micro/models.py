from micro.database import db
import logging

"""Microservice models definition."""


def batch_the_offer(product_id, time, payload):
    """Batch the object to simple dictionary."""
    batch = payload
    batch["vendor_id"] = batch["id"]
    del batch["id"]
    batch["timestamp"] = time
    batch["product_id"] = product_id
    return batch


class Product(db.Model):
    """Product model represents a product that can be offered"""

    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(128), unique=True, nullable=False)
    offers = db.relationship("Offer", backref="product")

    @classmethod
    def iterate_all(cls):
        for p in cls.query.all():
            yield p


class Offer(db.Model):
    """Offer is actual information about vendor details of a Product"""

    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    items_in_stock = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    timestamp = db.Column(db.DateTime)

    @classmethod
    def stage_offers(cls, product_id, time, payload):
        if payload["status_code"] == 200:
            for item in payload["data"]:
                batch = batch_the_offer(product_id, time, item)
                o = cls(**batch)
                db.session.add(o)
        else:
            url = payload["url"]
            code, msg = payload["data"]["code"], payload["data"]["msg"]
            logging.error(
                f"Failed to fetch data from URL`{url}`; {code}: {msg}"
            )

    @classmethod
    def commit(cls):
        db.session.commit()


class Client(db.Model):
    """Simple client model to hold UUID saved as 32 char string"""

    id = db.Column(db.String(32), primary_key=True, nullable=False)
