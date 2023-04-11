from django.db import models


class Collection(models.Model):
    vendor = models.ForeignKey('accounts.User', on_delete=models.PROTECT)
    name = models.CharField(max_length=128)
    brand = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    release_date = models.DateField()

    def __str__(self) -> str:
        return self.name


class Watch(models.Model):
    collection = models.ForeignKey(
        'watches.Collection', on_delete=models.PROTECT, related_name='watches',
        null=True, blank=True,
    )
    name = models.CharField(max_length=128)
    model = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    release_date = models.DateField()
    description = models.CharField(max_length=512)
    specifications = models.CharField(max_length=512)
    stock = models.IntegerField()

    def __str__(self) -> str:
        return self.name
