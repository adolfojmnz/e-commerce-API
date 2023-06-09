from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAdminUser,
)

from inventory.models import InventoryItem
from inventory.api.serializers import InventoryItemSerializer


class PermissionMixin:

    def get_permissions(self):
        if not self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class InventoryItemListView(PermissionMixin, ListCreateAPIView):
    model = InventoryItem
    queryset = model.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = []


class InventoryItemSingleView(PermissionMixin, RetrieveUpdateDestroyAPIView):
    model = InventoryItem
    queryset = model.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = []
