from django.urls import path
from .views import *
from users.models import User
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('profile/update/', cache_page(60 * 10)(UserProfileUpdateView.as_view()), name='profile-update'),
    path('me/', cache_page(60 * 10)(UserMeView.as_view()), name='profile'),
    path('register/', cache_page(60 * 10)(UserRegisterView.as_view()), name='register'),
    path('wholesaler-otp/', cache_page(60 * 10)(WholesalerOTPVerificationView.as_view()), name='register'),
    path('login/', cache_page(60 * 10)(UserLoginView.as_view()), name='login'),
    path('logout/', cache_page(60 * 10)(UserLogoutView.as_view()), name='logout'),
    path('forgot-password/', cache_page(60 * 10)(ForgotPasswordView.as_view()), name='forgot-password'),
    path('confirm-code/', cache_page(60 * 10)(ConfirmCodeView.as_view()), name='confirm-code'),
    path('change-forgot-password/', cache_page(60 * 10)(ChangeForgotPasswordView.as_view()), name='change-forgot-password'),
    path('change-password/', cache_page(60 * 10)(ChangePasswordView.as_view()), name='change-password'),
    path('user-list/', cache_page(60 * 10)(UserListView.as_view()), name='user-list'),

]


