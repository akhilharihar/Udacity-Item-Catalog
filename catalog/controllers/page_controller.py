from .category_controller import CategoryController
from .item_controller import ItemController
from app.utils import response, render
from flask import request, flash, redirect, url_for


class PageController:

    @staticmethod
    def index(category_name=None):
        categories = CategoryController.index()

        page = request.args.get('page', 1)
        per_page = request.args.get('per_page', 15)

        if category_name:
            url_category = " ".join(category_name.split('_'))
            db_category = CategoryController.get_by_name(url_category)
            db_items = ItemController.index(db_category.id, page=page,
                                            per_page=per_page)
        else:
            db_items = ItemController.index(page=page, per_page=per_page)

        return response(render('catalog/items_list.html',
                               current_category=category_name,
                               items=db_items, categories=categories))

    @staticmethod
    def show_item(item_id):
        item = ItemController.get(ItemController.decode_id(item_id))
        return response(render('catalog/show_item.html', item=item))

    @staticmethod
    def delete_item(item_id):
        item = ItemController.get(ItemController.decode_id(item_id), True)

        result = ItemController.delete(item)

        if result['result']:
            flash(result['message'], 'success')
        else:
            flash(result['message'], 'form_error')

        return redirect(url_for('catalog.catalog'))

    @staticmethod
    def create_item():
        if request.method == 'POST':
            return PageController.store_item()

        categories = CategoryController.index()
        return response(render('catalog/add_item.html',
                               categories=categories))

    @staticmethod
    def store_item():
        result = ItemController.store()

        if result['result']:
            message = 'Item {} added \
                successfully'.format(result['message'].name)

            flash(message, 'success')
            return redirect(url_for('catalog.show_item',
                                    item_id=result['message'].hash_id))

        else:
            flash(result['message'], 'form_error')
            print(result['message'])

            return redirect(url_for('catalog.create_item'))

    @staticmethod
    def edit_item(item_id):
        if request.method == 'POST':
            item = ItemController.get(ItemController.decode_id(item_id), True)
            return PageController.update_item(item)

        item = ItemController.get(ItemController.decode_id(item_id))
        categories = CategoryController.index()

        return response(render('catalog/edit_item.html', item=item,
                               categories=categories))

    @staticmethod
    def update_item(item):

        result = ItemController.update(item)

        if result['result']:
            message = 'Item {} updated \
                successfully'.format(result['message'].name)

            flash(message, 'success')
            return redirect(url_for('catalog.show_item',
                                    item_id=result['message'].hash_id))

        else:
            flash(result['message'], 'form_error')

            print(result['message'])

            return redirect(url_for('catalog.edit_item', item_id=item.hash_id))
