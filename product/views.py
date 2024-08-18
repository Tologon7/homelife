from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from drf_yasg.utils import swagger_auto_schema
from .pagination import CustomPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from product.serializers import *


class HomepageView(APIView):
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = ProductFilter

    def get(self, request, *args, **kwargs):
        new_products = Product.objects.all().order_by('-id')
        promotion_products = Product.objects.filter(promotion__isnull=False)
        popular_products = Product.objects.filter(id=1)

        new_serializer = ProductSerializer(new_products, many=True)
        promotion_serializer = ProductSerializer(promotion_products, many=True)
        popular_serializer = ProductSerializer(popular_products, many=True)

        response_data = {
            "homepage": {
                "promotion": promotion_serializer.data,
                "popular": popular_serializer.data,
                "new": new_serializer.data
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @swagger_auto_schema(
        tags=['category'],
        operation_description="Этот эндпоинт позволяет получить список всех категорий и создать новую категорию."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['category'],
        operation_description="Этот эндпоинт позволяет создать новую категорию."
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @swagger_auto_schema(
        tags=['category'],
        operation_description="Этот эндпоинт позволяет получить, обновить или удалить категорию по ID."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['category'],
        operation_description="Этот эндпоинт позволяет обновить категорию по ID."
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['category'],
        operation_description="Этот эндпоинт позволяет удалить категорию по ID."
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class BrandListCreateView(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    @swagger_auto_schema(
        tags=['brand'],
        operation_description="Этот эндпоинт позволяет получить список всех брендов и создать новый бренд."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['brand'],
        operation_description="Этот эндпоинт позволяет создать новый бренд."
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class BrandDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    @swagger_auto_schema(
        tags=['brand'],
        operation_description="Этот эндпоинт позволяет получить, обновить или удалить бренд по ID."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['brand'],
        operation_description="Этот эндпоинт позволяет обновить бренд по ID."
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['brand'],
        operation_description="Этот эндпоинт позволяет удалить бренд по ID."
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ColorListCreateView(generics.ListCreateAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

    @swagger_auto_schema(
        tags=['color'],
        operation_description="Этот эндпоинт позволяет получить список всех цветов и создать новый цвет."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['color'],
        operation_description="Этот эндпоинт позволяет создать новый цвет."
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ColorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

    @swagger_auto_schema(
        tags=['color'],
        operation_description="Этот эндпоинт позволяет получить, обновить или удалить цвет по ID."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['color'],
        operation_description="Этот эндпоинт позволяет обновить цвет по ID."
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['color'],
        operation_description="Этот эндпоинт позволяет удалить цвет по ID."
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    @swagger_auto_schema(
        tags=['product'],
        operation_description="Этот эндпоинт позволяет получить список всех продуктов и создать новый продукт."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['product'],
        operation_description="Этот эндпоинт позволяет создать новый продукт."
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @swagger_auto_schema(
        tags=['product'],
        operation_description="Этот эндпоинт позволяет получить, обновить или удалить продукт по ID."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['product'],
        operation_description="Этот эндпоинт позволяет обновить продукт по ID."
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['product'],
        operation_description="Этот эндпоинт позволяет удалить продукт по ID."
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ProductNewlView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter


    @swagger_auto_schema(
        tags=['product'],
        operation_description="Этот эндпоинт позволяет получить список новинок продуктов, и создать новый продукт."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['product'],
        operation_description="Этот эндпоинт позволяет создать новый продукт."
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        return Product.objects.all().order_by('-id')


class ProductPromotionView(generics.ListAPIView):
    queryset = Product.objects.filter(promotion__isnull=False)
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    @swagger_auto_schema(
        tags=['product'],
        operation_description="Этот эндпоинт позволяет получить список товаров с акциями."
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProductPopularView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    @swagger_auto_schema(
        tags=['product'],
        operation_description="Этот эндпоинт позволяет получить список популярных товаров."
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProductCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.filter(id=1)
    serializer_class = ProductCreateSerializer

    @swagger_auto_schema(
        tags=['product'],
        operation_description="Этот эндпоинт позволяет создать новый продукт."
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
