from django.urls import path
from .views import RegisterView, LoginAPIView, VerifyEmail, PasswordTokenCheckAPIView, RequestPasswordResetAPIView, \
    SetNewPasswordAPIView, VerifyEmailResend, GetUserProfileAPIView, UserViewSet, UpdateAdminData
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

    # Modify the user clinic or doctor status
    # Adaugă pagină de profil pentru - pagina
    path('update-user-profile-type/', UserViewSet.as_view(), name='modify-user-profile'),

    # Date administrator - page - clinica
    path('update-admin-data/', UpdateAdminData.as_view(), name='update-admin-data'),

    # Date administrator - page - clinica
    path('update-clinic-type-data/', UpdateAdminData.as_view(), name='update-admin-data')
]