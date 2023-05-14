from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=512)

    def __str__(self) -> str:
        return self.name
