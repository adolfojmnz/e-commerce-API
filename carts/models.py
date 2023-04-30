from django.db import models


class Cart(models.Model):
    user = models.ForeignKey('accounts.User',
                             on_delete=models.PROTECT,
                             related_name='cart')
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
    added_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        # Ensure that a product can only be added once to a cart.
        unique_together = ['cart', 'product']

    def __str__(self) -> str:
        return f"""
            {self.cart.user.username.capitalize()}\'s cart item |
            cart item No. {self.pk}
        """

