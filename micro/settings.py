import os
from micro import app
from dotenv import load_dotenv

ENV = load_dotenv(os.path.join(os.getcwd(), '.env'))

VARIABLES = [
    'DATABASE',
    'OFFERS_TOKEN'
]


def parse_env(key):
    value = os.environ.get(key)
    if value is None:
        raise KeyError(f'The enviroment variable {key} does not exist, please specify it')
    else:
        return key, os.environ.get(key)


class Config:
     def __init__(self, config_pair):
         for (k, v) in config_pair:
             setattr(self, k, v)


CONFIG = Config((map(parse_env, VARIABLES)))
