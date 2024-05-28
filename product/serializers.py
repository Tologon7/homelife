from rest_framework import serializers
from .models import *


class ProductAttributeSerializer(serializers.ModelSerializer):
    attribute_name = serializers.ReadOnlyField(source='attribute.name')

    class Meta:
        model = ProductAttribute
        fields = ['attribute_name', 'value']


class ProductSerializer(serializers.ModelSerializer):
    attributes = ProductAttributeSerializer(source='productattribute_set', many=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        attributes_data = validated_data.pop('productattribute_set', [])
        product = Product.objects.create(**validated_data)
        for attribute_data in attributes_data:
            attribute_name = attribute_data.get('attribute_name')
            attribute, created = Attribute.objects.get_or_create(name=attribute_name)
            ProductAttribute.objects.create(product=product, attribute=attribute, value=attribute_data.get('value'))
        return product


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'parent', 'children']

    def get_children(self, obj):
        return CategorySerializer(obj.children.all(), many=True).data if obj.children.exists() else []


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['id', 'name']
