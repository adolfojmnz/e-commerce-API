from django.urls import path

from inventory.api import views


urlpatterns = [
    path('inventory-items', views.InventoryItemListView.as_view(), name='inventory-items'),
    path('inventory-items/<int:pk>', views.InventoryItemSingleView.as_view(), name='inventory-item-detail'),
]
