from django.urls import path

from carts.api import views


urlpatterns = [
    path('carts', views.CartListView.as_view(), name='carts'),
    path('carts/<int:pk>', views.CartSingleView.as_view(), name='cart-detail'),
    path('cart-items', views.CartItemListView.as_view(), name='cart-items'),
    path('cart-items/<int:pk>', views.CartItemSingleView.as_view(), name='cart-item-detail'),
]
