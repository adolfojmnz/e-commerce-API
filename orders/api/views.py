from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)

from orders.models import Order, OrderItem
from orders.api.serializers import OrderSerializer, OrderItemSerializer


class OrderListView(ListCreateAPIView):
    model = Order
    queryset = model.objects.all()
    serializer_class = OrderSerializer


class OrderSingleView(RetrieveUpdateDestroyAPIView):
    model = Order
    queryset = model.objects.all()
    serializer_class = OrderSerializer


class OrderItemListView(ListCreateAPIView):
    model = OrderItem
    queryset = model.objects.all()
    serializer_class = OrderItemSerializer


class OrderItemSingleView(RetrieveUpdateDestroyAPIView):
    model = OrderItem
    queryset = model.objects.all()
    serializer_class = OrderItemSerializer

