from django.urls import path

from accounts.api import views

from accounts.api.views import CustomTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenBlacklistView,
)


urlpatterns = [
    path('users', views.UserListView.as_view(), name='users'),
    path('users/current', views.CurrentUserView.as_view(), name='current-user'),
    path('users/<int:pk>', views.UserDetailView.as_view(), name='user-detail'),

    # JWT Routes
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

]
