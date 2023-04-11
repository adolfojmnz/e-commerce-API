from django.db import models


class Review(models.Model):
    watch = models.ForeignKey(
        'watches.Watch', on_delete=models.PROTECT, related_name='reviews',
    )
    user = models.ForeignKey('accounts.User', on_delete=models.PROTECT)
    title = models.CharField(max_length=64)
    text = models.CharField(max_length=512)
    rating = models.IntegerField()
    date = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.text[:100]
