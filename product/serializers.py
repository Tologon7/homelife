from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'parent', 'category']

    def get_category(self, obj):
        if obj.category.exists():
            return CategorySerializer(obj.category.all(), many=True).data
        return []
