from django.db import models


class Cart(models.Model):
    user = models.ForeignKey('accounts.User',
                             on_delete=models.PROTECT,
                             related_name='carts')
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user.username.capitalize()}\'s shopping cart'


class CartItem(models.Model):
    cart = models.ForeignKey('carts.Cart',
                             on_delete=models.PROTECT,
                             related_name='cart_items')
    product = models.ForeignKey('products.Product',
                                on_delete=models.PROTECT,
                                related_name='cart_items')
    quantity = models.IntegerField()
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    added_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"""
            {self.cart.user.username.capitalize()}\'s cart item |
            cart item No. {self.pk}
        """

