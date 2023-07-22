from rest_framework import serializers

from inventory.models import InventoryItem


class InventoryItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryItem
        fields = '__all__'
        extra_kwargs = {
            'quantity': {'min_value': 0},
            'product': {'read_only': True},
            'updated_on': {'read_only': True},
            'added_on': {'read_only': True},
        }
