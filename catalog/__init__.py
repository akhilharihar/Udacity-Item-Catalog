from app.config import Blueprint
from .routes import web_routes, api_routes
from api import api

__all__ = ['catalog_application']

catalog_application = Blueprint('catalog', __name__, url_prefix='/catalog',
                                template_folder='templates')


catalog_application.add_url_rules(web_routes)
api.add_url_rules(api_routes)
