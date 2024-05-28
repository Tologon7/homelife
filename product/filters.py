import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['icontains'],
            'category': ['exact'],
            'price': ['lt', 'gt'],
            'attributes__attribute__name': ['exact'],
            'attributes__value': ['icontains'],
        }
