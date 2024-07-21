from django.urls import path
from .views import *

urlpatterns = [
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile-update'),
    path('profile/', UserMeView.as_view(), name='profile'),
    path('register/', UserRegisterUserView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('confirm-code/', ConfirmCodeView.as_view(), name='confirm-code'),
    path('change-forgot-password/', ChangeForgotPasswordView.as_view(), name='change-forgot-password'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
