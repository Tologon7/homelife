from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import *
from users.serializers import *
from rest_framework import generics, exceptions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


class RegisterView():
    pass


class LoginView():
    pass


class LogoutView():
    pass


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
