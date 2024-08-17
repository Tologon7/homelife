from django.urls import path
from .views import *

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('brands/', BrandListCreateView.as_view(), name='brand-list'),
    path('brands/<int:pk>/', BrandDetailView.as_view(), name='brand-detail'),
    path('colors/', ColorListCreateView.as_view(), name='color-list'),
    path('colors/<int:pk>/', ColorDetailView.as_view(), name='color-detail'),
    path('homepage/', HomepageView.as_view(), name='homepage'),
    path('all/', ProductListView.as_view(), name='product-all'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('new/', ProductNewlView.as_view(), name='product-new'),
    path('popular/', ProductPopularView.as_view(), name='product-popular'),
    path('promotions/', ProductPromotionView.as_view(), name='product-promotions'),
]
