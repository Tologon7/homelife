from django.urls import path
from product.views import *
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('categories/', cache_page(60 * 10)(CategoryListCreateView.as_view()), name='category-list'),
    path('categories/<int:pk>/', cache_page(60 * 10)(CategoryDetailView.as_view()), name='category-detail'),
    path('brands/', cache_page(60 * 10)(BrandListCreateView.as_view()), name='brand-list'),
    path('brands/<int:pk>/', cache_page(60 * 10)(BrandDetailView.as_view()), name='brand-detail'),
    path('colors/', cache_page(60 * 10)(ColorListCreateView.as_view()), name='color-list'),
    path('colors/<int:pk>/', cache_page(60 * 10)(ColorDetailView.as_view()), name='color-detail'),
    path('homepage/', cache_page(60 * 10)(HomepageView.as_view()), name='homepage'),
    path('all/', cache_page(60 * 10)(ProductListView.as_view()), name='product-all'),
    path('<int:pk>/', cache_page(60 * 10)(ProductDetailView.as_view()), name='product-detail'),
    path('create/', cache_page(60 * 10)(ProductCreateView.as_view()), name='product-create'),
    path('new/', cache_page(60 * 10)(ProductNewView.as_view()), name='product-new'),
    path('popular/', cache_page(60 * 10)(ProductPopularView.as_view()), name='product-popular'),
    path('promotions/', cache_page(60 * 10)(ProductPromotionView.as_view()), name='product-promotions'),
    # path('day/', ProductDayView.as_view(), name='product-of-the-day'),
    path('review/', cache_page(60 * 10)(ReviewCreateView.as_view()), name='create-review'),
    path('review/<int:pk>/', cache_page(60 * 10)(ReviewDetailView.as_view()), name='review-detail'),
]
