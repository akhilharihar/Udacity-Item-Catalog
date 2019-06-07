from app.config import Blueprint

__all__ = ['api']

_namespace = 'api'

_version = 'v1'

_api_url = '/{}/{}'.format(_namespace, _version)

api = Blueprint('api', __name__, url_prefix=_api_url)
