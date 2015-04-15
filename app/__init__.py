from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
cache = Cache(app,config={'CACHE_TYPE': 'simple'})

from app import views, models