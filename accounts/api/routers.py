from django.urls import path

from accounts.api import views

from accounts.api.views import CustomTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenBlacklistView,
)


urlpatterns = [
    path('users/current', views.CurrentUserView.as_view(), name='current-user'),

    path('admins', views.AdminListView.as_view(), name='admins'),
    path('admins/<int:pk>', views.AdminDetailView.as_view(), name='admin-detail'),

    path('customers', views.CustomerListView.as_view(), name='customers'),
    path('customers/<int:pk>', views.CustomerDetailView.as_view(), name='customer-detail'),

    # JWT Routes
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

]
