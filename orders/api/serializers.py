from django.db.models import Sum
from django.urls import reverse

from rest_framework import serializers

from orders.models import Order, OrderItem

from products.models import Product


class OrderSerializer(serializers.ModelSerializer):

    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True,
    )
    order_items = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    def get_order_items(self, order):
        return [
            self.context['request'].build_absolute_uri(
                reverse('order-item-detail', kwargs={'pk': order_item.pk})
            )
            for order_item in order.order_items.all()
        ]

    def get_total(self, order):
        return order.order_items.aggregate(Sum('sub_total'))['sub_total__sum']

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_items', 'total', 'created_on', 'updated_on']
        extra_kwargs = {
            'total': {'read_only': True},
            'created_on': {'read_only': True},
            'updated_on': {'read_only': True},
        }


class OrderItemSerializer(serializers.ModelSerializer):

    order = serializers.HyperlinkedRelatedField(
        view_name='order-detail',
        queryset=Order.objects.all(),
    )
    product = serializers.HyperlinkedRelatedField(
        view_name='product-detail',
        queryset=Product.objects.all(),
    )

    class Meta:
        model = OrderItem
        fields = '__all__'
        extra_kwargs = {
            'product_values': {'read_only': True},
            'sub_total': {'read_only': True},
            'added_on': {'read_only': True},
            'updated_on': {'read_only': True},
        }
