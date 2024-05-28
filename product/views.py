from rest_framework import generics
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(parent=None)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'color', 'price']


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class AttributeListCreateView(generics.ListCreateAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


class AttributeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
