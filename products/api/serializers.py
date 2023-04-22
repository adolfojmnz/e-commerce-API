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

    def get_available(self, obj):
        return obj.inventory.quantity > 0

    def get_quantity(self, obj):
        return obj.inventory.quantity

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'brand', 'description', 'specifications',
            'price', 'vendor', 'category', 'available', 'quantity',
        ]

