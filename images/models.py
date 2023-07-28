from django.db import models


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}: {self.image.url}'