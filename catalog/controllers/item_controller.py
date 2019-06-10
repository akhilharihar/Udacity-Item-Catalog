from catalog.models import Item, ItemHash, CategoryHash
from math import ceil
from flask import abort
from catalog.forms import ItemForm
from app.database import db


class ItemController:
    @staticmethod
    def index(category_id=None, page=1, per_page=15):
        """
        Get items from database. If category_id is not specified, recently
        added items are returned.
        params:
        category_id(int),
        page(int): current page.
        per_page(int): results per page.

        rtype: dict.
        """
        if not category_id:
            db_items = Item.query.order_by(Item.created_on.desc())
        else:
            db_items = Item.query.filter_by(category_id=category_id)

        try:
            page = int(page)
            if page < 0:
                raise ValueError('Page should be a positive number.')
        except (TypeError, ValueError):
            abort(400, 'Page should be a positive number.')

        try:
            per_page = int(per_page)
            if per_page < 0:
                raise ValueError('per_page should be a positive number.')
        except (TypeError, ValueError):
            abort(400, 'per_page should be a positive number.')

        data = db_items.paginate(page, per_page)

        unfiltered_items = data.items

        items = list()

        for x in unfiltered_items:
            items.append({
                'id': x.hash_id,
                'name': x.name,
                'category_id': x.category.hash_id,
                'category_name': x.category.name,
                'url_safe_category_name': "_".join(x.category.name.split(' '))
            })

        total_pages = ceil(data.total/data.per_page)

        result = dict(
            current_page=data.page,
            per_page=data.per_page,
            total=data.total,
            data=items,
            total_pages=total_pages
        )

        return result

    @staticmethod
    def get(item_id, return_model=False):
        """
        Get item. Return dict if return_model is true
        """
        item = Item.query.get_or_404(item_id)

        if return_model:
            return item

        return ItemController.item_to_dict(item)

    @staticmethod
    def store(user_id):
        """
        Store item to database.

        params:
        user_id: foreign key that should exists in table users.id
        """
        form = ItemForm()
        if not form.validate():
            return ItemController.message(False, form.errors)

        item = Item()
        item.name = form.name.data.strip()
        item.description = form.description.data
        item.category_id = CategoryHash.decode(form.category_id.data)
        item.user_id = user_id

        db.session.add(item)

        if item.commit_changes():
            return ItemController.message(True, item)
        else:
            return ItemController.message(False, 'Could not save \
            the given item.')

    @staticmethod
    def update(item):
        """
        Update item details.
        """

        form = ItemForm(id=item.id)

        if not form.validate():
            return ItemController.message(False, form.errors)

        item.name = form.name.data.strip()
        item.description = form.description.data
        item.category_id = CategoryHash.decode(form.category_id.data)

        db.session.add(item)

        if item.commit_changes():
            return ItemController.message(True, item)
        else:
            return ItemController.message(False, 'Could not save \
            the given item.')

    @staticmethod
    def delete(item):
        """
        Delete item from database.
        """
        name = item.name
        db.session.delete(item)

        try:
            db.session.commit()
            return ItemController.message(True, 'deleted \
                item {}.'.format(name))
        except Exception as e:
            db.session.rollback()
            print(e)
            return ItemController.message(False, 'could not \
                delete {}.'.format(name))

    @staticmethod
    def decode_id(id):
        """
        Deobfuscate item hash id
        """
        return ItemHash.decode(id)

    @staticmethod
    def message(is_success, message):
        if is_success:
            result = True
        else:
            result = False

        return {
            'result': result,
            'message': message
        }

    @staticmethod
    def item_to_dict(item):
        """
        Helper to convert item model instance to dict.
        """
        return dict(
            id=item.hash_id,
            name=item.name,
            description=item.description,
            category_id=item.category.hash_id,
            category_name=item.category.name,
            url_safe_category_name="_".join(item.category.name.split(' ')),
            created_on=item.created_on.strftime("%B %Y"),
            user_id=item.user_id
        )
