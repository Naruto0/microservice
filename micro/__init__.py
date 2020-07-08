from flask import Flask

app = Flask(__name__)

from micro.database import db
from micro.models import *
from micro.views import *
