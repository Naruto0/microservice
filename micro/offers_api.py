import requests

from micro.settings import CONFIG

API_URL = CONFIG.API_URL
headers = {"Bearer": CONFIG.OFFERS_TOKEN}

"""Remote API package layer."""


def get_offers(item):
    """Get offers from remote API based on product id"""
    action = f"{API_URL}/products/{item}/offers"
    request = requests.get(action, headers=headers)
    payload = {
        "status_code": request.status_code,
        "data": request.json(),
        "url": action,
    }
    return payload


def register_item(id, name, description):
    """Register product with remote API"""
    action = f"{API_URL}/products/register"
    data = {"id": id, "name": name, "description": description}
    request = requests.post(action, headers=headers, data=data)
    return request
