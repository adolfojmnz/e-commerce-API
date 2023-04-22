from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)

from carts.models import Cart, CartItem
from carts.api.serializers import CartSerializer, CartItemSerializer


class CartListView(ListCreateAPIView):
    model = Cart
    queryset = model.objects.all()
    serializer_class = CartSerializer


class CartSingleView(RetrieveUpdateDestroyAPIView):
    model = Cart
    queryset = model.objects.all()
    serializer_class = CartSerializer


class CartItemListView(ListCreateAPIView):
    model = CartItem
    queryset = model.objects.all()
    serializer_class = CartItemSerializer


class CartItemSingleView(RetrieveUpdateDestroyAPIView):
    model = CartItem
    queryset = model.objects.all()
    serializer_class = CartItemSerializer

