from django.db import models


class InventoryItem(models.Model):
    product = models.ForeignKey('products.Product',
                                on_delete=models.PROTECT,
                                related_name='inventory',
                                unique=True)
    quantity = models.IntegerField(default=0)
    added_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateField(auto_now=True)

    def __str__(self) -> str: 
        return f"""
            vendor: {self.product.vendor.username.capitalize()}
            | product: {self.product.name}
            | quantity: {self.quantity}
        """

    class Meta:
        verbose_name = 'Inventory Item'
        verbose_name_plural = 'Inventory Items'
        ordering = ['-added_on']
