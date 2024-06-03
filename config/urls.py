from django.contrib import admin
from django.urls import path
from django.urls import path, include
import certifi


urlpatterns = [
    path('admin/', admin.site.urls),

    #apps
    path('product/', include('product.urls')),
    path('users/', include('users.urls')),
    path('cart/', include('cart.urls')),

    #auth
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls'))

]
