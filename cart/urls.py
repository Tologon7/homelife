from django.urls import path
from .views import *


urlpatterns = [

    path('carts/', CartView.as_view()),


]