from django.urls import path

from products.api import views


urlpatterns = [
    path('products', views.ProductListView.as_view(), name='products'),
    path('products/<int:pk>', views.ProductSingleView.as_view(), name='product-detail'),
]
