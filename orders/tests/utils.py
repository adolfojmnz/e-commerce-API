from accounts.tests.utils import create_customer

from products.tests.utils import create_product

from carts.tests.utils import create_cart

from orders.models import Order, OrderItem


def create_order():
    order = Order.objects.create(
        user = create_customer(),
    )
    order.save()
    return order

def create_order_item():
    product = create_product()
    order_item = OrderItem.objects.create(
        order = create_order(),
        product = product,
        quantity = 10,
        sub_total = product.price * 10,
    )
    order_item.save()
    return order_item

