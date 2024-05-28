from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    title = models.CharField(max_length=200)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        unique_together = ('parent', 'title')
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title


class Attribute(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Color(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    promotion = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    description = models.TextField(max_length=2551)
    attributes = models.ManyToManyField(Attribute, through='ProductAttribute')

    def __str__(self):
        return self.title


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.product.title} - {self.attribute.name}: {self.value}"
