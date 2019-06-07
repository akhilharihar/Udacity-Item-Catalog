from app.database.db_seed import AbstractSeeder
from catalog.models import Category, Item
import random


class CategorySeeder(AbstractSeeder):
    model = Category

    def data(self):

        return {
            'name': self.fake.bs()
        }


class ItemSeeder(AbstractSeeder):
    model = Item

    def data(self):
        return {
            'name': self.fake.name(),
            'description': ' '.join(self.fake.paragraphs(nb=10)),
            'category_id': random.choice(Category.all()).id
        }
