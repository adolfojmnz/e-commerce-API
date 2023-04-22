from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.api.routers')),
    path('api/', include('products.api.routers')),
    path('api/', include('categories.api.routers')),
    path('api/', include('carts.api.routers')),
]

