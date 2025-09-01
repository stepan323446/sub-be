from django.urls import path
from .views import *

urlpatterns = [
    # Auth
    path('auth/token/', MyTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('auth/token/refresh/', MyTokenRefreshView.as_view(), name='token-refresh'),
    path('auth/token/verify/', MyTokenVerifyView.as_view(), name='token-verify'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('auth/verification-code-verify/', VerificationCodeVerify.as_view(), name='verification-code-verify'),
    path('auth/reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('auth/activate-user/', ActivateUserView.as_view(), name='activate-user'),

    # Users
    path('users/user-info/', UserInfoView.as_view(), name='user-info'),
    path('users/change-email/', ChangeEmailView.as_view(), name='change-email'),
    path('users/change-password/', ChangePasswordView.as_view(), name='change-password'),

    # Admin
    path('admin/users/<int:pk>', AdminUserInfo.as_view(), name="admin-user-info"),
    path('admin/users/<int:pk>/change-password/', AdminChangePassword.as_view(), name="admin-change-password/"),
    path('admin/users/<int:pk>/login/', AdminLoginAsUser.as_view(), name='admin-user-login'),
    path('admin/users/', AdminUserList.as_view(), name='admin-user-list'),
]