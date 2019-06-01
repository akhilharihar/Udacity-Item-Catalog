from app.config import Blueprint

__all__ = ['catalog_application']

catalog_application = Blueprint('catalog', __name__,
                                template_folder='templates')
