from django.urls import path

from carts.api import views


urlpatterns = [
    # Endpoint to be used by logged customers
    path('cart', views.CustomerCartView.as_view(), name='customer-cart'),
    path('cart/items', views.CustomerCartItemListView.as_view(), name='customer-cart-items'),
    path('cart/items/<int:pk>', views.CustomerCartItemSingleView.as_view(), name='customer-cart-item-detail'),

    # Endpoints to be used by admins
    path('carts', views.CartListView.as_view(), name='carts'),
    path('carts/<int:pk>', views.CartSingleView.as_view(), name='cart-detail'),
    path('cart-items', views.CartItemListView.as_view(), name='cart-items'),
    path('cart-items/<int:pk>', views.CartItemSingleView.as_view(), name='cart-item-detail'),
]
