from django_filters import rest_framework as filters
from .models import Product

class ProductFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category__value', lookup_expr='iexact')
    brand = filters.CharFilter(field_name='brand__value', lookup_expr='iexact')
    color = filters.CharFilter(field_name='color__value', lookup_expr='iexact')
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category', 'brand', 'color', 'price_min', 'price_max']
