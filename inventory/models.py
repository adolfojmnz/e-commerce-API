from django.db import models


class Inventory(models.Model):
    vendor = models.ForeignKey('accounts.User',
                               on_delete=models.PROTECT,
                               related_name='inventory')
    product = models.ForeignKey('products.Product',
                                on_delete=models.PROTECT,
                                related_name='inventory')
    quantity = models.IntegerField()
    added_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateField(auto_now=True)

    class Meta:
        unique_together = ['vendor', 'product']

    def __str__(self) -> str:
        return f"""
            vendor: {self.vendor.username.capitalize()}
            | product: {self.product.name}
            | quantity: {self.quantity}
        """

