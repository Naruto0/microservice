from flask import Flask
from micro.settings import CONFIG

app = Flask(__name__)

# from micro.database import db
from micro.models import *
from micro.views import *

logging.basicConfig(filename=CONFIG.APP_LOG, level=logging.ERROR)