from rest_framework import serializers
from .models import Product, Color, Category, Brand

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["title"]

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["title"]

class ColorSerializer(serializers.ModelSerializer):  # Поправлено на ColorSerializer
    class Meta:
        model = Color
        fields = ["title"]

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    color = ColorSerializer()
    brand = BrandSerializer()

    class Meta:
        model = Product
        fields = ['id', 'title', 'category', 'color', 'price', 'promotion', 'brand', 'quantity', 'description']
