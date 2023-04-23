from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework import status
from rest_framework.response import Response

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

    def post(self, request, *args, **kwargs):
        serializer = CartItemSerializer(data=request.data,
                                        context={'request': request})
        if serializer.is_valid():
            product = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']
            serializer.validated_data['sub_total'] = (
                product.price * quantity
            )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemSingleView(RetrieveUpdateDestroyAPIView):
    model = CartItem
    queryset = model.objects.all()
    serializer_class = CartItemSerializer
