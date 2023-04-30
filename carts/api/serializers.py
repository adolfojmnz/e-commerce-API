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
        """ Calculate the total price of all cart items in a cart by
            multiplying the quantity of each cart item by the price of the
            product it is associated with and then summing the results.
        """
        total = 0
        for cart_item in cart.cart_items.all():
            total += cart_item.quantity * cart_item.product.price
        return total

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
    sub_total = serializers.SerializerMethodField()

    def get_sub_total(self, cart_item):
        return cart_item.quantity * cart_item.product.price

    class Meta:
        model = CartItem
        fields = [
            'id', 'cart', 'product', 'quantity',
            'sub_total', 'added_on', 'updated_on',
        ]
        extra_kwargs = {
            # 'sub_total': {'read_only': True},
            'added_on': {'read_only': True},
            'updated_on': {'read_only': True},
        }
