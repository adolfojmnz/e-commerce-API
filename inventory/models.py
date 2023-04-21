from django.db import models


class Inventory(models.Model):
    product = models.ForeignKey('products.Product',
                                on_delete=models.PROTECT,
                                related_name='inventory')
    quantity = models.IntegerField(default=0)
    added_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f"""
            vendor: {self.vendor.username.capitalize()}
            | product: {self.product.name}
            | quantity: {self.quantity}
        """

