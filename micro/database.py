from flask_sqlalchemy import SQLAlchemy
from micro import app

db = app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalog.db'
db = SQLAlchemy(app)