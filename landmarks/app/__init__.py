import config
import os
from flask import (
    Flask,
    request)
from app import models
from app.extensions import (
    db,
    migrate,
    limiter
)
from app.api import api as api_bp
from app.errors import errors as error_bp


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    register_blueprints(app)
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    return None


def register_blueprints(app):
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(error_bp, url_prefix='/errors')
    return None
