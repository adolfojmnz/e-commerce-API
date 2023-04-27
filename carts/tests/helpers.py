from accounts.tests.helpers import UserTestMixin

from products.tests.helpers import create_product

from carts.models import Cart, CartItem


def create_cart(user=None):
    cart = Cart.objects.create(
        user = user or UserTestMixin().create_customer(),
    )
    cart.save()
    return cart

def create_cart_item(cart=None, product=None, quantity=10):
    product = product or create_product()
    cart_item = CartItem.objects.create(
        cart = cart or create_cart(),
        product = product,
        quantity = quantity,
        sub_total = product.price * quantity,
    )
    cart_item.save()
    return cart_item

