from django.db import models


class WatchPhoto(models.Model):
    watch = models.ForeignKey('watches.Watch',
                              on_delete=models.PROTECT,
                              related_name='photos')
    main = models.BooleanField(default=False)
    file = models.ImageField(upload_to='watches/')

    def __str__(self) -> str:
        return f'Watch `{self.watch.name}` photo {self.pk}'
