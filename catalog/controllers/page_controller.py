from .category_controller import CategoryController as CCT
from .item_controller import ItemController as ICT
from app.utils import response, render, url
from flask import request, flash, redirect
from flask_login import login_required, current_user


class PageController:

    @staticmethod
    def index(category_name=None):
        categories = CCT.index()

        page = request.args.get('page', 1)
        per_page = request.args.get('per_page', 15)

        if category_name:
            url_category = " ".join(category_name.split('_'))
            db_category = CCT.get_by_name(url_category)
            db_items = ICT.index(db_category.id, page=page,
                                 per_page=per_page)
        else:
            db_items = ICT.index(page=page, per_page=per_page)

        return response(render('catalog/items_list.html',
                               current_category=category_name,
                               items=db_items, categories=categories))

    @staticmethod
    def show_item(item_id):
        item = ICT.get(ICT.decode_id(item_id))
        return response(render('catalog/show_item.html', item=item))

    @staticmethod
    @login_required
    def delete_item(item_id):
        item = ICT.get(ICT.decode_id(item_id), True)

        if current_user.id != item.user_id:
            flash('No permission grant to delete this item.', 'form_error')
            return redirect(url('catalog.show_item',
                                item_id=item.hash_id))

        result = ICT.delete(item)

        if result['result']:
            flash(result['message'], 'success')
        else:
            flash(result['message'], 'form_error')

        return redirect(url('catalog.catalog'))

    @staticmethod
    @login_required
    def create_item():
        if request.method == 'POST':
            return PageController.store_item()

        categories = CCT.index()
        return response(render('catalog/add_item.html',
                               categories=categories))

    @staticmethod
    def store_item():
        result = ICT.store(current_user.id)

        if result['result']:
            message = 'Item {} added \
                successfully'.format(result['message'].name)

            flash(message, 'success')
            return redirect(url('catalog.show_item',
                                item_id=result['message'].hash_id))

        else:
            flash(result['message'], 'form_error')
            print(result['message'])

            return redirect(url('catalog.create_item'))

    @staticmethod
    @login_required
    def edit_item(item_id):
        item = ICT.get(ICT.decode_id(item_id), True)

        if current_user.id != item.user_id:
            flash('No permission grant to modify this item.', 'form_error')
            return redirect(url('catalog.show_item',
                                item_id=item.hash_id))

        if request.method == 'POST':
            return PageController.update_item(item)

        item = ICT.item_to_dict(item)

        categories = CCT.index()

        return response(render('catalog/edit_item.html', item=item,
                               categories=categories))

    @staticmethod
    def update_item(item):

        result = ICT.update(item)

        if result['result']:
            message = 'Item {} updated \
                successfully'.format(result['message'].name)

            flash(message, 'success')
            return redirect(url('catalog.show_item',
                                item_id=result['message'].hash_id))

        else:
            flash(result['message'], 'form_error')

            print(result['message'])

            return redirect(url('catalog.edit_item', item_id=item.hash_id))
