from django.contrib import admin
from django.urls import path
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    #apps
    path('product/', include('product.urls')),
    # path('users/', include('users.urls')),
    # path('cart/', include('cart.urls')),


]
