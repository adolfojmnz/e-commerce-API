from categories.models import Category

from categories.tests.data import single_category_data


def create_category():
    category = Category.objects.create(**single_category_data)
    category.save()
    return category

