from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import *
from rest_framework import generics, exceptions
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from .serializers import *
# from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import generics, status
from config import settings
from users.models import User, OTP

from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, NotAcceptable
from rest_framework.response import Response
from rest_framework import generics, exceptions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


class UserMeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_description="Этот ендпоинт предоставляет "
                              "возможность получить информацию "
                              "о текущем аутентифицированном пользователе. ",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserProfileUpdateView(generics.GenericAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность аутентифицированным "
                              "пользователям обновить свой профиль, "
                              "предоставив новые данные. После успешного "
                              "обновления профиля, система возвращает "
                              "сообщение об успешном обновлении.",
    )
    def put(self, request):
        user = request.user

        serializer = UserProfileSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User updated successfully!'}, status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterUserView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'user': UserRegistrationSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            return Response({
                'access': str(data['access']),
                'refresh': str(data['refresh']),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(generics.GenericAPIView):
    serializer_class = UserLogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_logout(serializer.validated_data['refresh'])
        return Response(status=status.HTTP_205_RESET_CONTENT)

    def perform_logout(self, refresh_token):
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            raise serializers.ValidationError({'refresh': str(e)})


class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_description="Этот эндпоинт предназначен "
                              "для пользователей, которые "
                              "забыли свой пароль. Пользователь "
                              "может запросить восстановление пароля, "
                              "предоставив свой номер телефона. Система якобы "
                              "отправит SMS с 4-значным кодом для восстановления "
                              "пароля, но на самом деле код будет храниться на "
                              "сервере для последующей проверки. После успешной "
                              "отправки номера телефона "
                              "система возвращает айди пользователя. \nКод подтверждения: 1991.",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
            otp_code = OTP.generate_otp()
            OTP.objects.create(user=user, otp=otp_code)
            # Send the OTP to the user's email
            subject = 'Forgot Password OTP'
            message = f'Your OTP is: {otp_code}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)

            return Response({"message": "OTP sent to your email."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmCodeView(generics.GenericAPIView):
    serializer_class = ConfirmationCodeSerializer

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_description="Этот эндпоинт позволяет "
                              "подтвердить код подтверждения, "
                              "который был отправлен на адрес "
                              "электронной почты пользователя "
                              "после успешной регистрации. После "
                              "подтверждения кода, система выдает новый "
                              "токен доступа (Access Token) и обновления "
                              "(Refresh Token) для пользователя.",
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data.get('code')
        try:
            confirmation_code = OTP.objects.get(otp=code)
        except OTP.DoesNotExist:
            return Response({"error": "Invalid or already confirmed code."}, status=400)

        user = confirmation_code.user
        confirmation_code.delete()

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Code confirmed successfully.",
            'user_id': str(user.id),
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })


class ChangeForgotPasswordView(generics.GenericAPIView):
    serializer_class = ChangeForgotPasswordSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_description="Этот эндпоинт предоставляет пользователям"
                              " возможность пользователям восстановить "
                              "свой пароль. Пользователь должен предоставить "
                              "новый пароль. После успешного восстановления пароля, пользователь "
                              "получит сообщение о том, что пароль был успешно изменен.",
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user

        user.set_password(serializer.validated_data['password'])
        user.save()

        return Response({
            'message': 'The password has been successfully changed.'
        }, status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    http_method_names = ['put']

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_description="Этот эндпоинт предоставляет возможность "
                              "зарегистрированным пользователям изменить "
                              "свой пароль. Пользователь должен предоставить "
                              "новый пароль. После успешной смены пароля, пользователь "
                              "получит сообщение о том, что пароль был успешно изменен.",
    )
    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user

        user.set_password(serializer.validated_data['password'])
        user.save()

        return Response({
            'message': 'The password has been successfully changed.'
        }, status=status.HTTP_200_OK)
