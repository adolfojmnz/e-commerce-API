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
        """ Returns a list containing the absolute urls
            for each cart item
        """
        return [
            self.context['request'].build_absolute_uri(
                reverse('cart-item-detail', kwargs={'pk': cart_item.pk})
            ) for cart_item in cart.cart_items.all()
        ]

    def get_total(self, cart):
        """ Returns the total cost for all items in the cart """
        return sum([
            cart_item.quantity * cart_item.product.price
            for cart_item in cart.cart_items.all()
        ])

    class Meta:
        model = Cart
        fields = ['id', 'user', 'cart_items', 'total', 'updated_on']
        extra_kwargs = {
            'total': {'read_only': True},
            'updated_on': {'read_only': True},
        }


class CartItemSerializer(serializers.ModelSerializer):

    product_name = serializers.SerializerMethodField()
    product_image = serializers.SerializerMethodField()
    product_brand = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()
    product_vendor = serializers.SerializerMethodField()
    product_available = serializers.SerializerMethodField()

    def get_product_name(self, cart_item):
        return cart_item.product.name

    def get_product_image(self, cart_item):
        return cart_item.product.image.url

    def get_product_brand(self, cart_item):
        return cart_item.product.brand

    def get_product_price(self, cart_item):
        return cart_item.product.price

    def get_product_vendor(self, cart_item):
        return cart_item.product.vendor.username

    def get_product_available(self, cart_item):
        return (cart_item.product.available and
                cart_item.product.inventory.quantity > 0)

    cart = serializers.HyperlinkedRelatedField(
        view_name='cart-detail',
        read_only=True,
    )
    product = serializers.HyperlinkedRelatedField(
        view_name='product-detail',
        read_only=True,
    )
    product_id = serializers.PrimaryKeyRelatedField(
        source='product',
        queryset=Product.objects.all(),
        write_only=True,
    )
    sub_total = serializers.SerializerMethodField()

    def get_sub_total(self, cart_item):
        return cart_item.quantity * cart_item.product.price

    class Meta:
        model = CartItem
        fields = [
            'id', 'cart', 'product', 'product_id', 'quantity', 'sub_total',
            'product_name', 'product_image', 'product_brand', 'product_price',
            'product_vendor', 'product_available', 'added_on', 'updated_on',
        ]
        extra_kwargs = {
            'added_on': {'read_only': True},
            'updated_on': {'read_only': True},
        }
        unique_together = ['cart', 'product_id']

    def unique_together_validation(self, attrs):
        """ Ensures that a product can only be added once to a cart """
        cart = attrs['cart']
        product = attrs['product']
        if cart.cart_items.filter(product=product).exists():
            raise serializers.ValidationError(
                {'message': 'This product is already in your cart.'}
            )
        return attrs

    def save(self, **kwargs):
        self.unique_together_validation(self.validated_data)
        return super().save(**kwargs)