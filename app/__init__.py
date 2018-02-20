from flask import Flask
from flask_elasticsearch import FlaskElasticsearch

es = FlaskElasticsearch()
app = Flask(__name__)
app.config.from_object('config')
es.init_app(app)

from app import views
