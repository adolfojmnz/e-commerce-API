from django.db.models import Sum
from django.urls import reverse

from rest_framework import serializers

from carts.models import Cart, CartItem

from products.models import Product

from accounts.models import User


class CartSerializer(serializers.ModelSerializer):

    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        queryset=User.objects.all(),
    )
    cart_items = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    def get_cart_items(self, cart):
        return [
            self.context['request'].build_absolute_uri(
                reverse('cart-item-detail', kwargs={'pk': cart_item.pk})
            )
            for cart_item in cart.cart_items.all()
        ]

    def get_total(self, cart):
        return cart.cart_items.aggregate(Sum('sub_total'))['sub_total__sum']

    class Meta:
        model = Cart
        fields = ['id', 'user', 'cart_items', 'total', 'updated_on']
        extra_kwargs = {
            'total': {'read_only': True},
            'updated_on': {'read_only': True},
        }


class CartItemSerializer(serializers.ModelSerializer):

    cart = serializers.HyperlinkedRelatedField(
        view_name='cart-detail',
        read_only=True,
    )
    product = serializers.HyperlinkedRelatedField(
        view_name='product-detail',
        queryset=Product.objects.all(),
    )

    class Meta:
        model = CartItem
        fields = '__all__'
        extra_kwargs = {
            'sub_total': {'read_only': True},
            'added_on': {'read_only': True},
            'updated_on': {'read_only': True},
        }
