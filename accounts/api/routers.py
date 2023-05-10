from django.urls import path

from .import views


urlpatterns = [
    path('users', views.UserListView.as_view(), name='users'),
    path('users/current', views.CurrentUserView.as_view(), name='current-user'),
    path('users/<int:pk>', views.UserDetailView.as_view(), name='user-detail'),
]
