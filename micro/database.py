from flask_sqlalchemy import SQLAlchemy
from micro import app
from micro.settings import CONFIG
"""Database definition"""

db = app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG.DATABASE
db = SQLAlchemy(app)
