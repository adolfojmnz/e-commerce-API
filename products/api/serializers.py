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
        queryset=Category.objects.all(),
    )
    available = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()

    def get_available(self, product):
        return product.inventory.quantity > 0 and product.available

    def get_quantity(self, product):
        return product.inventory.quantity

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'brand', 'image', 'description', 'specifications',
            'price', 'vendor', 'category', 'available', 'quantity',
        ]

