from abc import ABC, abstractmethod
from faker import Faker
from sqlalchemy import inspection, exc
from .connection import database as db
from pprint import pprint


class AbstractSeeder(ABC):
    """
    Abstract class to seed fake data to database.
    """

    def __init__(self):
        self.__fake = Faker()

    @property
    def fake(self):
        return self.__fake

    @property
    @abstractmethod
    def model(self):
        pass

    def seed(self, count=1, stdout=False):
        """
        Seed data to database.
        Params:
        count(int): Number of rows to insert to table
        stdout(bool): Print generated fake data to console.
        """
        try:
            inspection.inspect(self.model)
        except exc.NoInspectionAvailable as e:
            print('The given model class is not an instance of sqlalchemy')
            return {
                'error': True,
                'message': e
            }

        data = []
        for x in range(0, count):
            data.append(self.model(**self.data()))

        try:
            db.session.add_all(data)
            db.session.commit()
            if stdout:
                pprint(data)
            return {
                'error': False
            }

        except Exception as err:
            db.session.rollback()
            print(err)
            return {
                'error': True,
                'message': err
            }

    @abstractmethod
    def data(self):
        """
        Define data associated with the model. Should return a dict object
        with table :str: column and :str: values.
        """
        pass

    @classmethod
    def run(cls, count=1, stdout=False):
        self = cls()
        return self.seed(count, stdout)


__all__ = ['AbstractSeeder']
