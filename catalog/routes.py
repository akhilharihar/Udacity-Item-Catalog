from app.utils import Path
from .controllers.page_controller import PageController
from .controllers.json_controller import CategoryAPI, ItemAPI

__all__ = ['web_routes', 'api_routes']

web_routes = [
     Path(rule='/', endpoint='catalog',
          view_func=PageController.index),

     Path(rule='/category/<category_name>/items', endpoint='category_items',
          view_func=PageController.index),

     Path(rule='/item/new', endpoint='create_item',
          view_func=PageController.create_item, methods=['GET', 'POST']),

     Path(rule='/item/<item_id>', methods=['GET'],
          view_func=PageController.show_item, endpoint='show_item'),

     Path(rule='/item/<item_id>/delete', methods=['POST'],
          view_func=PageController.delete_item, endpoint='delete_item'),

     Path(rule='/item/<item_id>/edit', endpoint='edit_item',
          view_func=PageController.edit_item, methods=['GET', 'POST'])

]


api_routes = [
     Path(rule='/categories', endpoint='categories',
          view_func=CategoryAPI.index),

     Path(rule='/items', endpoint='items_in_catalog',
          view_func=ItemAPI.index),

     Path(rule='/items/<item_id>', endpoint='items',
          view_func=ItemAPI.get),
]
