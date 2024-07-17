from users.models import *
from rest_framework import serializers
from django.core.validators import RegexValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9!@#$%^&*()_+.-]+$',
                message='Username can only contain English letters, numbers, and special characters (!@#$%^&*()_+.-)',
            ),
        ],
        min_length=6,
        max_length=20,
    )

    class Meta:
        model = User
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.email)
        instance.email = validated_data.get('email', instance.email)

        instance.save()

        return instance
    