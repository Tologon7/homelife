from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from config import settings
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model

class Category(models.Model):
    label = models.CharField(max_length=200, unique=True)
    value = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.value:
            self.value = self.label.lower()

        # Проверяем, существует ли уже категория с таким label
        if Category.objects.filter(label=self.label).exclude(pk=self.pk).exists():
            raise ValidationError("Category with this label already exists.")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.label


class Brand(models.Model):
    label = models.CharField(max_length=200, unique=True)
    value = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.value:
            self.value = self.label.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.label


class Color(models.Model):
    label = models.CharField(max_length=200, unique=True)
    value = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.value:
            self.value = self.label.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.label


class Product(models.Model):

    title = models.CharField(max_length=255)
    image1 = CloudinaryField('image1')  # Используем CloudinaryField
    image2 = CloudinaryField('image2')
    image3 = CloudinaryField('image3')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', )
    color = models.ForeignKey(Color, on_delete=models.CASCADE, )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    promotion = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products', )
    quantity = models.IntegerField()
    description = models.TextField(max_length=2551)
    is_product_of_the_day = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    def save(self, *args, **kwargs):
        if self.quantity == 0:
            self.is_active = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    RATING_CHOICES = [
        (1, '1 star'),
        (1.5, '1.5 star'),
        (2, '2 star'),
        (2.5, '2.5 star'),
        (3, '3 star'),
        (3.5, '3.5 star'),
        (4, '4 star'),
        (4.5, '4.5 star'),
        (5, '5 star'),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Product"
    )
    user = models.ForeignKey(
        get_user_model(),  # Используйте get_user_model() вместо auth.User
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="User"
    )
    comments = models.TextField(verbose_name="Comments", blank=True, null=True)
    rating = models.FloatField(
        choices=RATING_CHOICES,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        verbose_name="Rating"
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    updated = models.DateTimeField(auto_now=True, verbose_name="Date Updated")

    def __str__(self):
        return f'Comment by {self.user} for {self.product} - Rating: {self.rating}'

class Banner(models.Model):
    image = CloudinaryField('image')

    def __str__(self):
        return f"Banner {self.image}"