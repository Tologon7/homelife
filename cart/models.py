# cart/models.py
from django.db import models
import uuid
from datetime import datetime


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def some_method(self):
        from product.models import Product  # Отложенный импорт
        product_instance = Product.objects.first()
        if product_instance:
            return f"Cart {self.id} contains {product_instance.title}"
        else:
            return f"Cart {self.id} is empty"

    def __str__(self):
        return str(self.id)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,  related_name="items", blank=True, null=True)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, blank=True, null=True, related_name="cartitems")
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"Cart: {self.cart}, Product: {self.product}"


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order {self.id}'
