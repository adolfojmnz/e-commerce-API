from django.urls import path

from carts.api import views


urlpatterns = [
    # Endpoint to be used by logged users (customers)
    path('cart', views.UserCartView.as_view(), name='user-cart'),
    path('cart/items', views.UserCartItemListView.as_view(), name='user-cart-items'),
    path('cart/items/<int:pk>', views.UserCartItemSingleView.as_view(),
                                name='user-cart-item-detail'),

    # Endpoints to be used by admins
    path('carts', views.CartListView.as_view(), name='carts'),
    path('carts/<int:pk>', views.CartSingleView.as_view(), name='cart-detail'),
    path('cart-items', views.CartItemListView.as_view(), name='cart-items'),
    path('cart-items/<int:pk>', views.CartItemSingleView.as_view(), name='cart-item-detail'),
]
