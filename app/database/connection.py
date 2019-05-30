from flask_sqlalchemy import SQLAlchemy, BaseQuery
from datetime import datetime


class ModelQuery(BaseQuery):
    """
    Augments the sqlalchemy base declarative class.
    """
    pass


database = SQLAlchemy(query_class=ModelQuery)


class DefaultTableMixin:
    """
    SQL Alchemy mixin class. Implement common database columns and model
    methods.
    """
    id = database.Column(database.Integer, primary_key=True)
    created_on = database.Column(database.DateTime, default=datetime.utcnow)
    updated_on = database.Column(database.DateTime, default=datetime.utcnow,
                                 onupdate=datetime.utcnow)

    def __repr__(self):
        class_name = self.__class__.__name__
        return "<{} {}>".format(class_name, self.id)

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def all(cls):
        return cls.query.all()

    @staticmethod
    def commit_changes():
        try:
            database.session.commit()
            return True
        except Exception as e:
            database.session.rollback()
            print(e)
            return False
