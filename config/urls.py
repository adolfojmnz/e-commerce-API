from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)


urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    # Apps URLs
    path('api/', include('accounts.api.routers')),
    path('api/', include('products.api.routers')),
    path('api/', include('categories.api.routers')),
    path('api/', include('inventory.api.routers')),
    path('api/', include('carts.api.routers')),
    path('api/', include('orders.api.routers')),
    path('api/', include('reviews.api.routers')),
    path('api/', include('images.api.routers')),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)