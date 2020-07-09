from micro.models import Product, Offer
from micro.offers_api import get_offers
from datetime import datetime


def process_offers(time=None):
    """Query and save offers for all Products"""
    if time is None:
        time = datetime.utcnow()
    for p in Product.iterate_all():
        payload = get_offers(p.id)
        Offer.stage_offers(p.id, time, payload)
    Offer.commit()


if __name__ == '__main__':
    process_offers()
