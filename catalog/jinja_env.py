from flask_login.mixins import AnonymousUserMixin


def is_item_owner(user, item_user_id):
    """
    check if current user is the owner of the item.
    """
    if isinstance(user, AnonymousUserMixin):
        return False

    if user.id == item_user_id:
        return True
    else:
        return False
