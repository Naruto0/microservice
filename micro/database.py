from flask_sqlalchemy import SQLAlchemy
from micro import app
from micro.settings import CONFIG
"""Database definition"""


app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG.DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


def init_db():
    db.create_all()
