from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page


urlpatterns = [

    path('carts/', cache_page(60 * 10)(CartView.as_view()), name='cart'),


]