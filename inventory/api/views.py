from rest_framework.generics import (
    ListAPIView, RetrieveUpdateAPIView
)
from rest_framework.permissions import IsAdminUser

from inventory.models import InventoryItem
from inventory.api.serializers import InventoryItemSerializer


class InventoryItemListView(ListAPIView):
    model = InventoryItem
    queryset = model.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAdminUser]


class InventoryItemSingleView(RetrieveUpdateAPIView):
    model = InventoryItem
    queryset = model.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAdminUser]

