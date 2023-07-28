from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAdminUser,
)

from categories.models import Category
from categories.api.serializers import CategorySerializer

from products.api.serializers import ProductSerializer


class PermissionMixin:

    def get_permissions(self):
        if not self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class CategoryListView(PermissionMixin, ListCreateAPIView):
    model = Category
    queryset = model.objects.all()
    serializer_class = CategorySerializer


class CategorySingleView(PermissionMixin, RetrieveUpdateDestroyAPIView):
    model = Category
    queryset = model.objects.all()
    serializer_class = CategorySerializer


class CategoryProductsView(ListAPIView):
    model = Category
    queryset = model.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []

    def get_queryset(self):
        category = self.model.objects.get(pk=self.kwargs['pk'])
        return category.products.all()