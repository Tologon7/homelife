from django.urls import path
from .views import *


urlpatterns = [
    path('list/', ProductAPIView.as_view(), name='product-list'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
]
