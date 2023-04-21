from django.urls import path

from categories.api import views


urlpatterns = [
    path('categories', views.CategoryListView.as_view(), name='categories'),
    path('categories/<int:pk>', views.CategorySingleView.as_view(), name='categorie-detail'),
]

