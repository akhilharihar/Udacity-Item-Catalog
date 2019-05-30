from .config.flask import Application
from settings import BaseConfig, ProductionConfig, DevelopmentConfig


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

    app.add_url_rule('/', 'index', index)

    return app


def index():
    return "flask app"