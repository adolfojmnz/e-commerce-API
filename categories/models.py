from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=256)
    products = models.ForeignKey('products.Product',
                                 on_delete=models.PROTECT,
                                 related_name='category')

    def __str__(self) -> str:
        return self.name
