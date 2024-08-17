from django.urls import path
from .views import *

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('colors/', ColorListCreateView.as_view(), name='color-list'),
    path('colors/<int:pk>/', ColorDetailView.as_view(), name='color-detail'),
    path('homepage/', HomepageView.as_view(), name='homepage'),
    path('list/', ProductListView.as_view(), name='product-list'),
    path('list/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('list/create/', ProductCreateView.as_view(), name='product-list-create'),
    path('list/new/', ProductNewlView.as_view(), name='product-list-new'),
    path('list/popular/', ProductPopularView.as_view(), name='product-list-popular'),
    path('list/promotions/', ProductPromotionView.as_view(), name='product-list-promotions'),
]
