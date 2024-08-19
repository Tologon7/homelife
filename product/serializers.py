from rest_framework import serializers
from .models import *


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ["title"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["title"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["title"]


class ReviewSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'rating', 'comments']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    color = ColorSerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    reviews = ReviewSummarySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'category',
            'color',
            'image',
            'price',
            'promotion',
            'brand',
            'quantity',
            'description',
            'is_product_of_the_day',
            'reviews',
        ]

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        color_data = validated_data.pop('color')
        brand_data = validated_data.pop('brand')

        category_instance, _ = Category.objects.get_or_create(**category_data)
        color_instance, _ = Color.objects.get_or_create(**color_data)
        brand_instance, _ = Brand.objects.get_or_create(**brand_data)

        product = Product.objects.create(
            category=category_instance,
            color=color_instance,
            brand=brand_instance,
            **validated_data

        )

        return product


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'category',
            'color',
            'image',
            'price',
            'promotion',
            'brand',
            'quantity',
            'description',
            'is_product_of_the_day'
        ]


class ReviewSerializer(serializers.ModelSerializer):

    product_title = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'product', 'product_title', 'user', 'user_name', 'comments', 'rating', 'created', 'updated']

    def get_product_title(self, obj):
        return obj.product.title if obj.product else 'unknown'

    def get_user_name(self, obj):
        return obj.user.first_name if obj.user else 'unknown'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('product', None)
        representation.pop('user', None)
        return representation