from accounts.tests.helpers import UserTestMixin

from products.tests.helpers import create_product

from orders.models import Order, OrderItem


def get_product_values(product):
    return {
        'name': product.name,
        'brand': product.brand,
        'description': product.description,
        'specifications': product.specifications,
        'price': str(product.price),
        'vendor': product.vendor.username,
    }


def create_order():
    order = Order.objects.create(
        user = UserTestMixin().create_customer(),
    )
    order.save()
    return order


def create_order_item():
    product = create_product()
    order_item = OrderItem.objects.create(
        order = create_order(),
        product = product,
        product_values = get_product_values(product),
        quantity = 10,
        sub_total = product.price * 10,
    )
    order_item.save()
    return order_item

