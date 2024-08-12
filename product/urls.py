from django.urls import path
from .views import *

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('colors/', ColorListCreateView.as_view(), name='color-list'),
    path('colors/<int:pk>/', ColorDetailView.as_view(), name='color-detail'),
    path('list/<int:product_id>', ProductListCreateViewID.as_view(), name='product-list'),
    path('list/', ProductListCreateView.as_view(), name='product-list'),
    path('list/new/', ProductNewlView.as_view(), name='product-list-new'),
    path('list/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]
