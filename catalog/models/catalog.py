from os import getenv
from app.database import db, DefaultTableMixin
from app.utils import AbstractHashID
from sqlalchemy.ext.hybrid import hybrid_property
from bleach import clean


class Category(db.Model, DefaultTableMixin):
    __tablename__ = 'categories'
    name = db.Column(db.String(100), unique=True, nullable=False)
    items = db.relationship('Item', backref='category', lazy=True)

    def __repr__(self):
        return "<Category {}>".format(self.name)

    @property
    def hash_id(self):
        if self.id:
            return CategoryHash.encode(self.id)
        else:
            return None


class Item(db.Model, DefaultTableMixin):
    __tablename__ = 'items'
    name = db.Column(db.String(250), nullable=False, unique=True)
    _description = db.deferred(db.Column(db.Text, default=None))
    category_id = db.Column(db.Integer,
                            db.ForeignKey('categories.id', ondelete='CASCADE'),
                            nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete='CASCADE'))

    def __repr__(self):
        return "<Item {}>".format(self.name)

    @hybrid_property
    def description(self):
        return self._description

    @description.setter
    def description(self, data):
        allowed_tags = ['h1', 'h2', 'h3', 'p', 'br', 'hr', 'strong', 'b',
                        'i', 'u', 'strike', 'blockquote', 'ol', 'li', 'pre']
        allowed_attr = {
            '*': ['style']
        }
        allowed_styles = ['color']

        cleaned = clean(data, tags=allowed_tags,
                        attributes=allowed_attr,
                        styles=allowed_styles)

        self._description = cleaned.encode('ascii', 'ignore').decode('ascii')

    @property
    def hash_id(self):
        if self.id:
            return ItemHash.encode(self.id)
        else:
            return None


class CategoryHash(AbstractHashID):
    salt = getenv('CATEGORY_SALT')
    min_length = 4


class ItemHash(AbstractHashID):
    salt = getenv('ITEM_SALT')
    min_length = 7
