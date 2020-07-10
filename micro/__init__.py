from flask import Flask
import logging

from micro.settings import CONFIG
from flask_migrate import Migrate

app = Flask(__name__)

from micro.models import *  # noqa: E402, F403, F401
from micro.views import *  # noqa: E402, F403, F401

from micro.database import db  # noqa: E402,

migrate = Migrate(app, db)

logging.basicConfig(filename=CONFIG.APP_LOG, level=logging.ERROR)
