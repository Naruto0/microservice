import os
from dotenv import load_dotenv

"""Package to load environment variables to application config variable based on `VARIABLES` list"""


load_dotenv(os.path.join(os.getcwd(), '.env'))

VARIABLES = [
    'DATABASE',
    'OFFERS_TOKEN',
    'API_URL'
]


def parse_env(key):
    value = os.environ.get(key)
    if value is None:
        raise KeyError(f'The environment variable {key} does not exist, please specify it')
    else:
        return key, os.environ.get(key)


class Config:
     def __init__(self, setting):
         for k, v in setting:
             setattr(self, k, v)


CONFIG = Config((map(parse_env, VARIABLES)))
