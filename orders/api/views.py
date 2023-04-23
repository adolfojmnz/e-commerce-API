from django.db.models import Q

from rest_framework.generics import (
    ListAPIView, RetrieveAPIView,
)
from rest_framework import status
from rest_framework.response import Response

from orders.models import Order, OrderItem
from orders.api.serializers import OrderSerializer, OrderItemSerializer


class OrderListView(ListAPIView):
    model = Order
    queryset = model.objects.all()
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data,
                                     context={'request': request})
        if serializer.is_valid():
            cart_items = request.user.cart.all()[0].cart_items.filter(
                Q(product__inventory__gt=0) & Q(product__available=True)
            )
            if not cart_items.exists():
                return Response(
                    {'error': 'No available items in cart.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.validated_data['user'] = request.user
            serializer.save()
            self.create_order_items(serializer.instance, cart_items)
            self.remove_cart_items(cart_items)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create_order_items(self, order, cart_items):
        for cart_item in cart_items:
            product = cart_item.product
            quantity = cart_item.quantity
            product_values = {
                'name': product.name,
                'brand': product.brand,
                'description': product.description,
                'specifications': product.specifications,
                'price': str(product.price),
                'vendor': product.vendor.username,
                'category': product.category.name,
            }
            OrderItem.objects.create(
                order=order,
                product=product,
                product_values=product_values,
                quantity=quantity,
                sub_total=product.price * quantity,
            )

    def remove_cart_items(self, cart_items):
        for cart_item in cart_items:
            cart_item.delete()


class OrderSingleView(RetrieveAPIView):
    model = Order
    queryset = model.objects.all()
    serializer_class = OrderSerializer


class OrderItemListView(ListAPIView):
    model = OrderItem
    queryset = model.objects.all()
    serializer_class = OrderItemSerializer


class OrderItemSingleView(RetrieveAPIView):
    model = OrderItem
    queryset = model.objects.all()
    serializer_class = OrderItemSerializer
