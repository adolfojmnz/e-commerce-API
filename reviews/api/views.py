from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)

from reviews.models import Review
from reviews.api.serializers import ReviewSerializer


class ReviewListView(ListCreateAPIView):
    model = Review
    queryset = model.objects.all()
    serializer_class = ReviewSerializer


class ReviewSingleView(RetrieveUpdateDestroyAPIView):
    model = Review
    queryset = model.objects.all()
    serializer_class = ReviewSerializer

