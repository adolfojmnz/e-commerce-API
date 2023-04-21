from accounts.tests.utils import (
    create_customer,
    create_vendor,
)

from carts.models import Cart, CartItem


def create_cart():
    cart = Cart.objects.create(
        user = create_customer(),
        total = 100.00,
    )
    cart.save()
    return cart


def create_cart_item():
    product = create_product(),
    cart_item = CartItem.objects.create(
        cart = create_cart(),
        product = product,
        quantity = 10,
        sub_total = product.price * 10,
    )
    cart_item.save()
    return cart_item()

