from .config.flask import Application
from settings import BaseConfig, ProductionConfig, DevelopmentConfig
from .database import db


def create_app():
    """
    Flask application factory.

    params:
    config (dict): Custom app configuration.
    """
    app = Application(__name__)

    app.config.from_object(BaseConfig)

    if app.config.get('ENV', 'development') == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    register_extensions(app)
    app.add_url_rule('/', 'index', index)

    return app


def register_extensions(flask_instance):
    """
    Register flask extensions.
    """
    db.init_app(flask_instance)


def index():
    return "flask app"
