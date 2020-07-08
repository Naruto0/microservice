import requests

from micro.settings import CONFIG

API_URL = CONFIG.API_URL
headers = {'Bearer': CONFIG.OFFERS_TOKEN}


def get_offers(item):
    action = f'{API_URL}/products/{item}/offers'
    request = requests.get(action, headers=headers)
    return request


def register_item(id, name, description):
    action = f'{API_URL}/products/register'
    body = {'id': id,
            'name': name,
            'descritpion': description
            }
    request = requests.post(action, headers=headers, body=body)
    return request