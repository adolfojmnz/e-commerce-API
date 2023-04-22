from django.urls import path

from orders.api import views


urlpatterns = [
    path('orders', views.OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>', views.OrderSingleView.as_view(), name='order-detail'),
    path('order-items', views.OrderItemListView.as_view(), name='order-items'),
    path('order-items/<int:pk>', views.OrderItemSingleView.as_view(), name='order-item-detail'),
]
