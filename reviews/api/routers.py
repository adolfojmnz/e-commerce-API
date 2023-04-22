from django.urls import path

from reviews.api import views


urlpatterns = [
    path('reviews', views.ReviewListView.as_view(), name='reviews'),
    path('reviews/<int:pk>', views.ReviewSingleView.as_view(), name='review-detail'),
]
