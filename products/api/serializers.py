from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):

    vendor = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True,
    )

    class Meta:
        model = Product
        fields = '__all__'

