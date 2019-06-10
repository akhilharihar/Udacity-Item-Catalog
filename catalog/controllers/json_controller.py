from .category_controller import CategoryController
from .item_controller import ItemController
from app.utils import json_response
from flask import request


class CategoryAPI:
    @staticmethod
    def index():
        """
        Get categories.
        """
        data = CategoryController.index()
        return json_response(data)


class ItemAPI:
    @staticmethod
    def index():
        """
        Get items form database. If category args is not provided, recently
        added items is returned.
        """
        page = 1
        per_page = 25

        if request.args.get('page'):
            page = request.args['page']

        if request.args.get('per_page'):
            per_page = request.args['per_page']

        category = request.args.get('category', None)

        if category:
            category = CategoryController.decode_id(category)

        data = ItemController.index(category_id=category, page=page,
                                    per_page=per_page)

        return json_response(data)

    @staticmethod
    def get(item_id):
        """
        Get a specific item
        """
        data = ItemController.get(ItemController.decode_id(item_id))

        data.pop('user_id', None)

        return json_response(data)
