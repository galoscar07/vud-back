from django.urls import path
from .views import RegisterView, LoginAPIView, VerifyEmail, PasswordTokenCheckAPIView, RequestPasswordResetAPIView, \
    SetNewPasswordAPIView, VerifyEmailResend, GetUserProfileAPIView, UserViewSet
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),

    path('login/', LoginAPIView.as_view(), name='login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh-token'),

    # Verify email
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('email-verify-resend/', VerifyEmailResend.as_view(), name='email-verify-resend'),

    # Password Reset
    path('password-reset-request/', RequestPasswordResetAPIView.as_view(), name='request-password-reset'),
    path('password-reset/<uidb>/<token>', PasswordTokenCheckAPIView.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),

    # Get user profile
    path('get-user-profile/', GetUserProfileAPIView.as_view(), name='get-user-profile'),

    # Modify the user teacher or student status
    path('update-user-profile/', UserViewSet.as_view(), name='modify-user-profile')
]