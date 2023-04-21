from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from categories.models import Category
from categories.api.serializers import CategorySerializer


class CategoryListView(ListCreateAPIView):
    model = Category
    queryset = model.objects.all()
    serializer_class = CategorySerializer


class CategorySingleView(RetrieveUpdateDestroyAPIView):
    model = Category
    queryset = model.objects.all()
    serializer_class = CategorySerializer

