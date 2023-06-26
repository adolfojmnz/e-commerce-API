from django.db.models import Q, F
from django.utils import timezone

from rest_framework.generics import (
    ListAPIView, RetrieveAPIView,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from orders.models import Order, OrderItem
from orders.api.serializers import OrderSerializer, OrderItemSerializer

from carts.models import Cart


class OrderListMixin:

    def get_cart_items(self, cart) -> list:
        """ Returns a queryset of cart items whose products are avalaible. """
        return cart.cart_items.filter(
            Q(product__available=True) &
            Q(product__inventory__quantity__gt=0) &
            Q(product__inventory__quantity__gte=F('quantity'))
        )

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

    def update_product_inventory(self, cart_items):
        for cart_item in cart_items:
            product = cart_item.product
            product.inventory.quantity -= cart_item.quantity
            product.inventory.save()

    def delete_cart_items(self, cart, cart_items):
        for cart_item in cart_items:
            cart_item.delete()
        cart.updated_on = timezone.now()
        cart.save()


class OrderListView(OrderListMixin, ListAPIView):
    model = Order
    queryset = model.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset

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
            self.update_product_inventory(cart_items)
            self.delete_cart_items(cart, cart_items)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderSingleView(RetrieveAPIView):
    model = Order
    queryset = model.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset


class OrderItemListView(ListAPIView):
    model = OrderItem
    queryset = model.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            order__user=self.request.user
        )
        if self.request.query_params.get('order'):
            queryset = queryset.filter(
                order__pk=self.request.query_params.get('order')
            )
        return queryset


class OrderItemSingleView(RetrieveAPIView):
    model = OrderItem
    queryset = model.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            order__user=self.request.user
        )
        return queryset
