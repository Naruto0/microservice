from flask import Flask

from micro.settings import CONFIG
from flask_migrate import Migrate

app = Flask(__name__)

from micro.models import *
from micro.views import *

from micro.database import db

migrate = Migrate(app, db)

logging.basicConfig(filename=CONFIG.APP_LOG, level=logging.ERROR)
