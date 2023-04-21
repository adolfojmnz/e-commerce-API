from rest_framework.generics import (
    ListAPIView, RetrieveUpdateDestroyAPIView
)

from products.models import Product
from products.api.serializers import ProductSerializer


class ProductListView(ListAPIView):
    model = Product
    queryset = model.objects.all()
    serializer_class = ProductSerializer


class ProductSingleView(RetrieveUpdateDestroyAPIView):
    model = Product
    queryset = model.objects.all()
    serializer_class = ProductSerializer

