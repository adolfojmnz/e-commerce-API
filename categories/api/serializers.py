from rest_framework import serializers

from categories.models import Category


class CategorySerializer(serializers.ModelSerializer):

    products_count = serializers.SerializerMethodField()

    def get_products_count(self, category):
        return category.products.count()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'products_count']

