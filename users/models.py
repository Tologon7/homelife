from django.db import models


class Gender(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Age(models.Model):
    title = models.IntegerField()

    def __str__(self):
        return self.title


class User(models.Model):
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    number = models.IntegerField()
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    age = models.ForeignKey(Age, on_delete=models.CASCADE)

    def __str__(self):
        return self.username
