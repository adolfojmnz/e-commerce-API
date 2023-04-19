from products.models import Product

from accounts.tests.utils import create_user

from products.tests.data import single_product_data


def create_product():
    vendor = create_user()
    single_product_data['vendor'] = vendor
    product = Product.objects.create(**single_product_data)
    product.save()
    return product

