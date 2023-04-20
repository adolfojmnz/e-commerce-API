from products.models import Product

from accounts.tests.utils import create_user

from categories.tests.utils import create_category

from products.tests.data import single_product_data


def create_product():
    vendor = create_user()
    category = create_category()
    single_product_data['vendor'] = vendor
    single_product_data['category'] = category
    product = Product.objects.create(**single_product_data)
    product.save()
    return product

