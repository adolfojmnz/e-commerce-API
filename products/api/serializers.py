from django.db.models import Avg

from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):

    available = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()

    def get_available(self, product):
        return int(product.inventory.quantity) > 0 and product.available

    def get_quantity(self, product):
        return product.inventory.quantity

    def get_rating(self, product):
        return product.reviews.aggregate(
            rating=Avg('rating')
        )['rating']

    def get_total_reviews(self, product):
        return product.reviews.count()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'brand', 'image_url', 'description', 'specifications',
            'price', 'vendor', 'category', 'available', 'quantity', 'rating',
            'total_reviews',
        ]
        extra_kwargs = {
            'vendor': {'read_only': True},
        }
