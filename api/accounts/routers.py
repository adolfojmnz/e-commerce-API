from django.urls import path

from api.accounts.views import UserListView


urlpatterns = [
    path('users', UserListView.as_view(), name='users'),
]
