from django.db.models import Sum

from rest_framework import serializers

from carts.models import Cart, CartItem

from products.models import Product


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

    cart = serializers.HyperlinkedRelatedField(
        view_name='cart-detail',
        queryset=Cart.objects.all(),
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
