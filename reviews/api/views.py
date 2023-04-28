from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
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


class ReviewListView(ReviewListMixin, ListCreateAPIView):
    model = Review
    queryset = model.objects.all()
    serializer_class = ReviewSerializer

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


class ReviewSingleView(RetrieveUpdateDestroyAPIView):
    model = Review
    queryset = model.objects.all()
    serializer_class = ReviewSerializer
