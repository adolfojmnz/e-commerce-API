from django.db.models import Avg
from django.urls import reverse

from rest_framework import serializers

from products.models import Product

from categories.models import Category


class ProductSerializer(serializers.ModelSerializer):

    vendor = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True,
    )
    category = serializers.HyperlinkedRelatedField(
        view_name='category-detail',
        read_only=True,
    )
    category_id = serializers.PrimaryKeyRelatedField(
        source='category',
        queryset=Category.objects.all(),
        write_only=True,
    )

    available = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()

    def get_available(self, product):
        return product.inventory.quantity > 0 and product.available

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
            'price', 'vendor', 'category', 'category_id', 'available', 'quantity', 'rating',
            'total_reviews',
        ]

