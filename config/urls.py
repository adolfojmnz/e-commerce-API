from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Apps URLs
    path('api/', include('accounts.api.routers')),
    path('api/', include('products.api.routers')),
    path('api/', include('categories.api.routers')),
    path('api/', include('inventory.api.routers')),
    path('api/', include('carts.api.routers')),
    path('api/', include('orders.api.routers')),
    path('api/', include('reviews.api.routers')),
]
