from app.config import Blueprint
from .routes import web_routes, api_routes
from api import api
from .jinja_env import is_item_owner

__all__ = ['catalog_application']

catalog_application = Blueprint('catalog', __name__, url_prefix='/catalog',
                                template_folder='templates')


catalog_application.add_url_rules(web_routes)
api.add_url_rules(api_routes)

catalog_application.add_app_template_global(is_item_owner, 'is_item_owner')
