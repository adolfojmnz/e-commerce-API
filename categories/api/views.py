from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from categories.models import Category
from categories.api.serializers import CategorySerializer

from products.api.serializers import ProductSerializer


class CategoryListView(ListCreateAPIView):
    model = Category
    queryset = model.objects.all()
    serializer_class = CategorySerializer


class CategorySingleView(RetrieveUpdateDestroyAPIView):
    model = Category
    queryset = model.objects.all()
    serializer_class = CategorySerializer


class CategoryProductsView(ListAPIView):
    model = Category
    queryset = model.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        category = self.model.objects.get(pk=self.kwargs['pk'])
        return category.products.all()