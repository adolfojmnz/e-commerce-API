from rest_framework.generics import (
    ListAPIView, RetrieveUpdateAPIView
)
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

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

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.get_object(),
                                        data=request.data,
                                        partial=True)
        if serializer.is_valid():
            if serializer.validated_data.get('quantity') is not None:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
