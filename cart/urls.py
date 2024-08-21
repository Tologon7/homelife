from django.urls import path
from cart.views import *
from django.views.decorators.cache import cache_page


urlpatterns = [

    path('carts/', cache_page(60 * 10)(CartView.as_view()), name='cart'),
    path('order/', cache_page(60 * 10)(CreateOrderView.as_view()), name='cart'),


]