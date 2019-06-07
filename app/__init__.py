from .config.flask import Application
from settings import static_file_url
from settings import BaseConfig, ProductionConfig, DevelopmentConfig
from .database import db, migrate
from .auth import login_manager, oauth
from .routes import url_rules
from api import api
from catalog import catalog_application


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

    app.register_blueprint(api)
    app.add_url_rules(url_rules)
    register_blueprints(app)

    return app


def register_extensions(flask_instance):
    """
    Register flask extensions.
    """
    db.init_app(flask_instance)
    migrate.migrations.init_app(flask_instance, db)
    login_manager.init_app(flask_instance)
    oauth.oauth.init_app(flask_instance)


def register_blueprints(flask_instance):
    flask_instance.register_blueprint(catalog_application)
