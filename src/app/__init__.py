import config
import os
from flask import (
    Flask,
    request)
from app import commands, models
from app.api import api as api_bp
from app.extensions import (
    db,
    migrate,
)

Config = eval(os.environ['FLASK_APP_CONFIG'])


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    register_blueprints(app)
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    patch_request_class(app)
    return None


def register_blueprints(app):
    app.register_blueprint(api_bp, url_prefix='/api')
    return None
