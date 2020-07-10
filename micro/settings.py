import os
from dotenv import load_dotenv

"""Package to load environment variables to application
config variable using `VARIABLES` list"""

load_dotenv(os.path.join(os.getcwd(), ".env"))

VARIABLES = ["DATABASE", "OFFERS_TOKEN", "API_URL", "APP_LOG"]


def parse_env(key):
    """Filter and combine VARIABLES key
    with corresponding `os.eniviron` value"""
    value = os.environ.get(key)
    if value is None:
        raise KeyError(
            f"The environment variable {key} does not exist, please specify it"
        )
    else:
        return key, os.environ.get(key)


class Config:
    """Meta class to make arbitrary ENVVARS
    as attribute rather than dict item"""

    def __init__(self, setting):
        for k, v in setting:
            setattr(self, k, v)


CONFIG = Config((map(parse_env, VARIABLES)))
