from django.db import models


class Review(models.Model):
    """
    Reviews require the order that the product was ordered in
    Args:
        - order (Order): The order that the product to review was was ordered in
        - product (Product): The product to review
        - user (User): The user that made the review
    """
    order = models.ForeignKey('orders.Order',
                               on_delete=models.PROTECT,
                               related_name='reviews')
    product = models.ForeignKey('products.Product',
                                 on_delete=models.PROTECT,
                                 related_name='reviews')
    user = models.ForeignKey('accounts.User',
                             on_delete=models.PROTECT,
                             related_name='reviews')
    title = models.CharField(max_length=64)
    text = models.CharField(max_length=2048)
    rating = models.IntegerField()
    date = models.DateField(auto_now=True)

    class Meta:
        """ Users can only review a product once (per order) """
        unique_together = ['order', 'product']

    def __str__(self) -> str:
        return self.text[:100]
