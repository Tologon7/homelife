from users.models import *
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from users.models import User, OTP
import re


class PasswordMixin(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"error": "Password fields didn't match."})

        password = attrs['password']
        if not re.search(r'[A-Z]', password):
            raise serializers.ValidationError({'password': "Password must contain at least one uppercase letter."})
        if not re.search(r'[!@#$%^&*]', password):
            raise serializers.ValidationError(
                {'password': "Password must contain at least one special character (!@#$%^&*)."})
        if len(password) < 8:
            raise serializers.ValidationError({'password': "Password must be at least 8 characters long."})
        return attrs



# profile
class UserSerializer(serializers.ModelSerializer):
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
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    number = serializers.IntegerField()
    wholesaler = serializers.BooleanField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'number', 'wholesaler']


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
        required=False
    )

    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    number = serializers.IntegerField(required=False)
    wholesaler = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'number', 'wholesaler']

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.number = validated_data.get('number', instance.number)
        instance.wholesaler = validated_data.get('wholesaler', instance.wholesaler)

        instance.save()
        return instance

# register
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    wholesaler = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'username', 'number', 'wholesaler', 'password']

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            username=validated_data.get('username', ''),
            number=validated_data.get('number', 0),
            wholesaler=validated_data.get('wholesaler', False),
        )
        return user

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        tokens = self.get_tokens_for_user(instance)
        representation.update(tokens)
        return representation


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Добавьте дополнительные поля в токен, если нужно
        return token


class UserLoginSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()


class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        try:
            token = RefreshToken(attrs['refresh'])
            token.blacklist()  # Поместите токен в черный список
        except Exception as e:
            raise serializers.ValidationError({'refresh': str(e)})
        return attrs


# forgot password
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ConfirmationCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4)

    def validate(self, data):
        code = data.get('code')

        try:
            otp_obj = OTP.objects.get(otp=code)
            if otp_obj.is_expired:
                raise serializers.ValidationError({'error': "OTP has expired."})
        except OTP.DoesNotExist:
            raise serializers.ValidationError({'error': "Invalid OTP."})

        return data


class ChangeForgotPasswordSerializer(serializers.ModelSerializer, PasswordMixin):
    class Meta:
        model = User
        fields = [
            'password',
            'confirm_password',
        ]


class ChangePasswordSerializer(serializers.ModelSerializer, PasswordMixin):
    old_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not check_password(value, user.password):
            raise serializers.ValidationError({"error": "Invalid old password."})
        return value

    class Meta:
        model = User
        fields = ['old_password', 'password', 'confirm_password']
