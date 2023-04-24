from django.db.models import Q
from django.utils import timezone

from rest_framework.generics import (
    ListAPIView, RetrieveAPIView,
)
from rest_framework import status
from rest_framework.response import Response

from orders.models import Order, OrderItem
from orders.api.serializers import OrderSerializer, OrderItemSerializer

from carts.models import Cart


class OrderListView(ListAPIView):
    model = Order
    queryset = model.objects.all()
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data,
                                     context={'request': request})
        if serializer.is_valid():
            cart = Cart.objects.get(user=request.user)
            cart_items = self.get_cart_items(cart)
            if not cart_items.exists():
                return Response(
                    {'error': 'No available items in cart.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.validated_data['user'] = request.user
            serializer.save()
            self.create_order_items(serializer.instance, cart_items)
            self.delete_cart_items(cart, cart_items)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_cart_items(self, cart):
        return cart.cart_items.filter(
            Q(product__inventory__gt=0) & Q(product__available=True)
        )

    def delete_cart_items(self, cart, cart_items):
        for cart_item in cart_items:
            cart_item.delete()
        cart.updated_on = timezone.now()
        cart.save()

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
