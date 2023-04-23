from django.db.models import Sum

from rest_framework import serializers

from orders.models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):

    total = serializers.SerializerMethodField()

    def get_total(self, order):
        return order.order_items.aggregate(Sum('sub_total'))['sub_total__sum']

    class Meta:
        model = Order
        fields = ['id', 'user', 'total', 'created_on', 'updated_on']
        extra_kwargs = {
            'total': {'read_only': True},
            'created_on': {'read_only': True},
            'updated_on': {'read_only': True},
        }


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'
