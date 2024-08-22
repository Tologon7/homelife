from rest_framework import serializers
from django.db.models import Avg
from .models import Product, Category, Color, Brand, Review
from .utils import round_to_nearest_half


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["title"]


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ["title"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["title"]


class ReviewSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'rating', 'comments']


# class ImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = [
#             'image1',
#             'image2',
#             'image3'
#         ]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    color = ColorSerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    reviews = ReviewSummarySerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()
    # images = ImageSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'category',
            'color',
            'image1',
            'image2',
            'image3',
            'price',
            'promotion',
            'brand',
            'quantity',
            'description',
            'is_product_of_the_day',
            'reviews',
            'avg_rating'
        ]

    def get_avg_rating(self, obj):
        # Здесь мы рассчитываем и округляем средний рейтинг
        if obj.reviews.exists():
            avg_rating = obj.reviews.aggregate(Avg('rating'))['rating__avg']
            return round_to_nearest_half(avg_rating)
        return 0


class ProductShortSerializer(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    # images = ImageSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'image1',
            'image2',
            'image3',
            'avg_rating',
            'title',
            'price',
            'promotion',
        ]

    def get_avg_rating(self, obj):
        if obj.reviews.exists():
            avg_rating = obj.reviews.aggregate(Avg('rating'))['rating__avg']
            return round_to_nearest_half(avg_rating)
        return 0


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'category',
            'color',
            'image1',
            'image2',
            'image3',
            'price',
            'promotion',
            'brand',
            'quantity',
            'description',
            'is_product_of_the_day'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not instance.reviews.exists():
            representation.pop('reviews', None)
        return representation


class ReviewSerializer(serializers.ModelSerializer):

    product_title = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id',
            'product',
            'product_title',
            'user',
            'user_name',
            'comments',
            'rating',
            'created',
            'updated'
        ]

    def get_product_title(self, obj):
        return obj.product.title if obj.product else 'unknown'

    def get_user_name(self, obj):
        return obj.user.first_name if obj.user else 'unknown'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('product', None)
        representation.pop('user', None)
        return representation
