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


def create_order(user=None):
    order = Order.objects.create(
        user = user or UserTestMixin().create_customer(),
    )
    order.save()
    return order


def create_order_item(product=None, order=None, quantity=10):
    product = product or create_product()
    order_item = OrderItem.objects.create(
        order = order or create_order(),
        product = product,
        product_values = get_product_values(product),
        quantity = quantity,
        sub_total = product.price * quantity,
    )
    order_item.save()
    return order_item

