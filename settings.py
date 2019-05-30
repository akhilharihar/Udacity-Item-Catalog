import os

__all__ = ['BASE_DIR', 'BaseConfig', 'ProductionConfig', 'DevelopmentConfig']

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    """
    Default flask instance configuration.
    """
    SECRET_KEY = os.getenv('APP_KEY')
    SERVER_NAME = os.getenv('SERVER_NAME')


class ProductionConfig:
    """
    Flask instance configuration in production.
    """
    USE_X_SENDFILE = True


class DevelopmentConfig:
    """
    Flask instance configuration for development.
    """
    pass
