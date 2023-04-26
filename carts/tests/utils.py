from accounts.tests.helpers import UserTestMixin

from products.tests.helpers import create_product

from carts.models import Cart, CartItem


def create_cart():
    cart = Cart.objects.create(
        user = UserTestMixin().create_customer(),
    )
    cart.save()
    return cart

def create_cart_item():
    product = create_product()
    cart_item = CartItem.objects.create(
        cart = create_cart(),
        product = product,
        quantity = 10,
        sub_total = product.price * 10,
    )
    cart_item.save()
    return cart_item

