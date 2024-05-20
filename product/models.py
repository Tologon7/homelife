from django.db import models
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    title = models.CharField(max_length=200)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='category')

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        unique_together = ('parent', 'title')
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title


class Color(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    color = models.ForeignKey('Color', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=255, decimal_places=2)
    promotion = models.DecimalField(max_digits=255, decimal_places=2)
    quantity = models.IntegerField()
    # characteristic = models.ForeignKey('Characteristic', on_delete=models.CASCADE)
    characteristic = models.TextField(max_length=2551)
    description = models.TextField(max_length=2551)
