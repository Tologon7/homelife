from django.contrib import admin
from .models import Category, Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'quantity', 'is_active']
    fields = ('title', 'image1', 'image2', 'image3', 'category', 'color', 'price', 'promotion', 'brand', 'quantity', 'description', 'is_product_of_the_day', 'is_active', )

admin.site.register(Category)

