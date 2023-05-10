from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

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