from django.db import models


class InventoryItem(models.Model):
    product = models.OneToOneField('products.Product',
                                on_delete=models.PROTECT,
                                related_name='inventory')
    quantity = models.IntegerField(default=0)
    added_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"product: {self.product.name} | quantity: {self.quantity}"

    class Meta:
        verbose_name = 'Inventory Item'
        verbose_name_plural = 'Inventory Items'
        ordering = ['-added_on']
