from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework import status
from rest_framework.response import Response

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

    def post(self, request, *args, **kwargs):
        serializer = OrderItemSerializer(data=request.data,
                                         context={'request': request})
        if serializer.is_valid():
            product = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']
            product_values = {
                'name': product.name,
                'brand': product.brand,
                'description': product.description,
                'specifications': product.specifications,
                'price': str(product.price),
                'vendor': product.vendor.username,
                'category': product.category.name,
            }
            serializer.validated_data['product_values'] = product_values
            serializer.validated_data['sub_total'] = (
                product.price * quantity
            )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderItemSingleView(RetrieveUpdateDestroyAPIView):
    model = OrderItem
    queryset = model.objects.all()
    serializer_class = OrderItemSerializer
