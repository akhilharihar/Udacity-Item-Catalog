from .config.flask import Application
from settings import static_file_url
from settings import BaseConfig, ProductionConfig, DevelopmentConfig
from .database import db, migrate
from .auth import login_manager


def create_app():
    """
    Flask application factory.

    params:
    config (dict): Custom app configuration.
    """
    static_url = static_file_url()

    app = Application(__name__, static_url_path=static_url)

    app.config.from_object(BaseConfig)

    if app.config.get('ENV', 'development') == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    register_extensions(app)

    register_blueprints(app)

    return app


def register_extensions(flask_instance):
    """
    Register flask extensions.
    """
    db.init_app(flask_instance)
    migrate.migrations.init_app(flask_instance, db)
    login_manager.init_app(flask_instance)


def register_blueprints(flask_instance):
    pass
