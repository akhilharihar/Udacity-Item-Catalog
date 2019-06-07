from catalog.models import Category, CategoryHash


class CategoryController:

    @staticmethod
    def index():
        db_categories = Category.all()

        categories = list()

        for x in db_categories:
            categories.append({
                'id': x.hash_id,
                'name': x.name,
                'url_safe_name': "_".join(x.name.split(' '))
            })

        return categories

    @staticmethod
    def get_by_name(name):
        return Category.query.filter_by(name=name).first_or_404()

    @staticmethod
    def decode_id(id):
        return CategoryHash.decode(id)
