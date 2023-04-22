from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)

from inventory.models import InventoryItem
from inventory.api.serializers import InventoryItemSerializer


class InventoryItemListView(ListCreateAPIView):
    model = InventoryItem
    queryset = model.objects.all()
    serializer_class = InventoryItemSerializer


class InventoryItemSingleView(RetrieveUpdateDestroyAPIView):
    model = InventoryItem
    queryset = model.objects.all()
    serializer_class = InventoryItemSerializer

