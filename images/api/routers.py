from django.urls import path

from images.api import views


urlpatterns = [
    path('images', views.Images.as_view(), name='images'),
]