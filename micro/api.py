from micro.settings import CONFIG


def callback():
    obsfucated = CONFIG.OFFERS_TOKEN[:-10] + 10 * '.'
    return f'Hello from api, the token is {obsfucated}'
