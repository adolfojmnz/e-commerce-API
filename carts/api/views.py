from rest_framework.generics import (
    ListAPIView, ListCreateAPIView,
    RetrieveAPIView, RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)

from carts.models import Cart, CartItem
from carts.api.serializers import CartSerializer, CartItemSerializer


class CartListView(ListAPIView):
    model = Cart
    queryset = model.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAdminUser]


class CartSingleView(RetrieveAPIView):
    model = Cart
    queryset = model.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAdminUser]


class CartItemListView(ListAPIView):
    model = CartItem
    queryset = model.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAdminUser]


class CartItemSingleView(RetrieveUpdateDestroyAPIView):
    model = CartItem
    queryset = model.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAdminUser]


class CustomerCartView(RetrieveAPIView):
    model = Cart
    queryset = model.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Cart.objects.get(user=self.request.user)


class CustomerCartItemListView(ListCreateAPIView):
    model = CartItem
    queryset = model.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart = Cart.objects.get(user=self.request.user)
        return CartItem.objects.filter(cart=cart)

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
            if not (serializer.validated_data['quantity'] <=
                    product.inventory.quantity):
                return Response(
                    {'message': 'Not enough quantity available'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart = Cart.objects.get(user=request.user)
            serializer.validated_data['cart'] = cart
            serializer.save()
            cart.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerCartItemSingleView(RetrieveDestroyAPIView):
    model = CartItem
    queryset = model.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart = Cart.objects.get(user=self.request.user)
        return CartItem.objects.get(cart=cart, pk=self.kwargs['pk'])

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance=instance,
                                           data=request.data,
                                           partial=True,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        new_quantity = serializer.validated_data.get('quantity')
        if new_quantity:
            quantity_in_stock = instance.product.inventory.quantity
            if not new_quantity <= quantity_in_stock:
                return Response(
                    {'message': 'Requested update quantity not available'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if serializer.validated_data.get('product'):
            return Response(
                {'message': 'Cart Item product cannot be updated'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
