from flask import Flask
from micro.settings import CONFIG

app = Flask(__name__)

from micro.models import *
from micro.views import *

from micro.database import init_db

init_db()

logging.basicConfig(filename=CONFIG.APP_LOG, level=logging.ERROR)
