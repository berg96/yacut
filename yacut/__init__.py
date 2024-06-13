from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

from settings import Config

SWAGGER_URL = '/api/docs'
API_DOCS_PATH = '/static/openapi.yml'


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.register_blueprint(get_swaggerui_blueprint(SWAGGER_URL, API_DOCS_PATH))

from . import api_views, error_handlers, views
