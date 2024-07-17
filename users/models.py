from django.db import models


class User(models.Model):
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    number = models.IntegerField()
    wholesaler = models.BooleanField()

    def __str__(self):
        return self.username
