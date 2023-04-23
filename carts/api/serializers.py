from django.db.models import Sum

from rest_framework import serializers

from carts.models import Cart, CartItem


class CartSerializer(serializers.ModelSerializer):

    total = serializers.SerializerMethodField()

    def get_total(self, cart):
        return cart.cart_items.aggregate(Sum('sub_total'))['sub_total__sum']

    class Meta:
        model = Cart
        fields = ['id', 'user', 'total', 'updated_on']
        extra_kwargs = {
            'total': {'read_only': True},
            'updated_on': {'read_only': True},
        }


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = '__all__'

