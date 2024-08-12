from django.urls import path
from .views import *
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('colors/', ColorListCreateView.as_view(), name='color-list'),
    path('colors/<int:pk>/', ColorDetailView.as_view(), name='color-detail'),
    path('list/<int:product_id>', ProductListCreateViewID.as_view(), name='product-list'),
    path('list/', ProductListCreateView.as_view(), name='product-list'),
    path('list/new/', ProductNewlView.as_view(), name='product-list-new'),
    path('list/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('review/', RatingViewSet.as_view({'get': 'list', 'post': 'create'}), name='review-list-create'),
    path('review/<int:pk>/', RatingViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='review-detail'),
] + debug_toolbar_urls()


#код бекса
# from rest_framework_nested import routers
# from django.urls import path, include
# from . import views
#
# router = routers.DefaultRouter()
# router.register(r'list', views.ProductViewSet, basename='product')
#
#
# product_router = routers.NestedDefaultRouter(router, r'list', lookup='product')
# product_router.register(r'ratings', views.RatingViewSet, basename='product-ratings')
#
# urlpatterns = [
#     path('', include(router.urls)),
#     path('', include(product_router.urls)),
# ]