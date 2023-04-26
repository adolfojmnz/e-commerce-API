from django.utils import timezone

from rest_framework.generics import (
    ListAPIView, RetrieveAPIView,
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework import status
from rest_framework.response import Response

from carts.models import Cart, CartItem
from carts.api.serializers import CartSerializer, CartItemSerializer


class CartListView(ListAPIView):
    model = Cart
    queryset = model.objects.all()
    serializer_class = CartSerializer


class CartSingleView(RetrieveAPIView):
    model = Cart
    queryset = model.objects.all()
    serializer_class = CartSerializer


class CartItemListView(ListCreateAPIView):
    model = CartItem
    queryset = model.objects.all()
    serializer_class = CartItemSerializer

    def post(self, request, *args, **kwargs):
        serializer = CartItemSerializer(data=request.data,
                                        context={'request': request})
        if serializer.is_valid():
            product = serializer.validated_data['product']
            if not (product.available and product.inventory.quantity > 0):
                return Response(
                    {'message': 'Product is not available'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart = Cart.objects.get(user=request.user)
            quantity = serializer.validated_data['quantity']
            serializer.validated_data['cart'] = cart
            serializer.validated_data['sub_total'] = (
                product.price * quantity
            )
            serializer.save()
            cart.updated_on = timezone.now()
            cart.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemSingleView(RetrieveUpdateDestroyAPIView):
    model = CartItem
    queryset = model.objects.all()
    serializer_class = CartItemSerializer
