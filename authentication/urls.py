from django.urls import path

from footerlabels.views import ClinicList, TopClinicsAPIView, ClinicDetailAPIView, ReviewCreate, DoctorList, \
    DoctorDetailAPIView, ReviewDoctorCreate
from .views import RegisterView, LoginAPIView, VerifyEmail, PasswordTokenCheckAPIView, RequestPasswordResetAPIView, \
    SetNewPasswordAPIView, VerifyEmailResend, GetUserProfileAPIView, UserViewSet, UpdateAdminData, UpdateClinicTypeData, \
    UpdateClinicProfileView, DeleteUserView, redeem_clinic_request, UpdateDoctorProfileView, redeem_doctor_request
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
    path('password-reset/<uidb>/<token>/', PasswordTokenCheckAPIView.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),

    # Delete Profile
    path('delete-profile/', DeleteUserView.as_view(), name='delete-profile'),

    # Get user profile
    path('get-user-profile/', GetUserProfileAPIView.as_view(), name='get-user-profile'),

    # Modify the user clinic or doctor status
    # Adaugă pagină de profil pentru - pagina
    path('update-user-profile-type/', UserViewSet.as_view(), name='modify-user-profile'),

    # Date administrator - page - clinica
    path('update-admin-data/', UpdateAdminData.as_view(), name='update-admin-data'),

    # Update doctor info
    path('update-doctor-profile/', UpdateDoctorProfileView.as_view(), name='update-doctor-profile'),

    # Date administrator - page - clinica
    path('update-clinic-type-data/', UpdateClinicTypeData.as_view(), name='update-admin-data'),
    path('update-clinic-profile/', UpdateClinicProfileView.as_view(), name='update-clinic-profile'),

    # Redeem clinic
    path('revendica-clinica/', redeem_clinic_request, name='redeem_clinic'),
    path('revendica-doctor/', redeem_doctor_request, name='redeem_doctor'),

    path('get-clinics/', ClinicList.as_view(), name='get-clinics-filters'),
    path('get-top-clinics/', TopClinicsAPIView.as_view(), name='get-top-clinics'),
    path('clinics/<int:id>/', ClinicDetailAPIView.as_view(), name='get-clinic-by-id'),
    path('clinic-review/', ReviewCreate.as_view(), name='create-clinic-review'),

    path('get-doctors/', DoctorList.as_view(), name='get-doctors-filters'),
    path('doctors/<int:id>/', DoctorDetailAPIView.as_view(), name='get-doctor-by-id'),
    path('doctor-review/', ReviewDoctorCreate.as_view(), name='create-doctor-review')
]
