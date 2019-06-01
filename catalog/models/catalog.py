from os import getenv
from app.database import db, DefaultTableMixin
from app.utils import AbstractHashID


class Category(db.Model, DefaultTableMixin):
    __tablename__ = 'categories'
    name = db.Column(db.String(100), unique=True, nullable=False)
    items = db.relationship('Item', backref='category', lazy=True)

    def __repr__(self):
        return "<Category {}>".format(self.name)

    @property
    def hash_id(self):
        return CategoryHash.encode(self.id)


class Item(db.Model, DefaultTableMixin):
    __tablename__ = 'items'
    name = db.Column(db.String(250), nullable=False, unique=True)
    description = db.deferred(db.Column(db.Text, default=None))
    category_id = db.Column(db.Integer,
                            db.ForeignKey('categories.id', ondelete='CASCADE'),
                            nullable=False)

    def __repr__(self):
        return "<Item {}>".format(self.name)

    @property
    def hash_id(self):
        return ItemHash.encode(self.id)


class CategoryHash(AbstractHashID):
    salt = getenv('CATEGORY_SALT')
    min_length = 4


class ItemHash(AbstractHashID):
    salt = getenv('ITEM_SALT')
    min_length = 7
