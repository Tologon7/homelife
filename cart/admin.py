from django.contrib import admin
from .models import Cart, CartItem
from product.models import Product



admin.site.register(Cart)


class CartItemAdmin(admin.ModelAdmin):
    model = CartItem
    # Ошибка может быть здесь, если используется какой-то компонент django-mptt для поля product

admin.site.register(CartItem, CartItemAdmin)