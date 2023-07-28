from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    SAFE_METHODS,
)

from orders.models import Order

from products.models import Product

from reviews.models import Review
from reviews.api.serializers import ReviewSerializer


class ReviewListMixin:

    def user_can_review(self, user, product_id, order_id):
        """ Check if the user made an order for this product """
        try:
            order = Order.objects.get(id=order_id)
            if not order.user == user:
                return False
            product = Product.objects.get(id=product_id)
            return order.order_items.filter(
                product=product
            ).exists()
        except Order.DoesNotExist:  # or Product.DoesNotExist
            return False

    def isinstance_of_int(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False


class ReviewListView(ReviewListMixin, ListAPIView):
    model = Review
    queryset = model.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        self.permission_classes = []
        if not self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def post(self, request, *args, **kwargs):
        if not self.user_can_review(request.user,
                                    request.data['product'],
                                    request.data['order']):
            return Response(
                {'message': 'You cannot review a product you did not order'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        """ Filter reviews by product """
        queryset = super().get_queryset()
        if self.request.query_params.get('product'):
            product_id = self.request.query_params.get('product')
            if self.isinstance_of_int(product_id):
                queryset = queryset.filter(product=product_id)
            else:
                queryset = queryset.none()
        return queryset


class ReviewSingleView(RetrieveUpdateDestroyAPIView):
    model = Review
    queryset = model.objects.all()
    serializer_class = ReviewSerializer

    def requesting_user_owns_review(self):
        """ Returns True if the requesting user owns the
            requested review, False otherwise or if the
            requested review does not exist. """
        try:
            return Review.objects.get(
                pk=self.request.parser_context['kwargs']['pk']
            ).user == self.request.user
        except Review.DoesNotExist:
            return False

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = []
        elif not self.requesting_user_owns_review():
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
