import django.db
import jwt
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer, \
    ResetPasswordEmailSerializer, SetNewPasswordSerializer, PasswordTokenCheckSerializer, \
    UserUpdateUserProfileSerializer, ClinicProfileSerializer, DoctorProfileSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import User, Clinic, Doctor
from .utils import Util


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token

        # TODO: Put FE link to redirect
        # current_site = get_current_site(request)
        # relative_link = reverse('email-verify')
        absolute_url = f'https://vud-fe.herokuapp.com/email-verification/?token={str(token)}'

        data = {
            'url': absolute_url,
            'email': user.email
        }
        user_data['link'] = absolute_url
        Util.send_email(data=data, email_type='verify-email')
        print(absolute_url)

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter('token',
                                           in_=openapi.IN_QUERY,
                                           description='Description',
                                           type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailResend(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        try:
            user = User.objects.get(email=request.data.get('email'))
            token = RefreshToken.for_user(user).access_token
            # current_site = get_current_site(request)
            # relative_link = reverse('email-verify')
            absolute_url = f'https://vud-fe.herokuapp.com/email-verification/?token={str(token)}'
            # absolute_url = f'http://{current_site}{relative_link}?token={str(token)}'

            data = {
                'url': absolute_url,
                'email': user.email
            }
            Util.send_email(data=data, email_type='verify-email')
            print(absolute_url)
            user_data['link'] = absolute_url

            return Response(user_data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response(user_data, status=status.HTTP_201_CREATED)
            pass


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailSerializer

    def post(self, request):
        data = {'request': request, 'data': request.data}
        email = request.data.get('email', '')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            # TODO: Put FE link to redirect
            current_site = get_current_site(request=request)
            relative_link = reverse('password-reset-confirm', kwargs={'uidb': uidb64, 'token': token})
            absolute_url = f'http://{current_site}{relative_link}'
            data = {
                'url': absolute_url,
                'email': user.email
            }
            Util.send_email(data=data, email_type='verify-email')
            print(absolute_url)

        return Response({'url': absolute_url}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPIView(generics.GenericAPIView):
    serializer_class = PasswordTokenCheckSerializer

    def get(self, request, uidb, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token not valid, please request a new one'})
            return Response({'success': True, 'message': 'Credentials Valid', 'uidb': uidb, 'token': token})
        except DjangoUnicodeDecodeError:
            return Response({'error': 'Token not valid, please request a new one'})
        except User.DoesNotExist:
            return Response({'error': 'Token not valid, please request a new one'})


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class GetUserProfileAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        # if the user is logged
        if user.is_authenticated:
            # if the user is a student
            if user.is_clinic:
                serializer = ClinicProfileSerializer(user.clinic_profile)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif user.is_doctor:
                serializer = DoctorProfileSerializer(user.doctor_profile)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No profile'}, status=401)
        return Response({'error': 'Authentication credentials were not provided.'}, status=401)


class UserViewSet(generics.GenericAPIView):
    serializer_class = UserUpdateUserProfileSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        user = request.user
        is_clinic = request.data.get('is_clinic', None)
        is_doctor = request.data.get('is_doctor', None)

        if is_clinic is not None:
            user.is_clinic = is_clinic
            try:
                clinic = Clinic.objects.create(user=user)
                clinic.save()
            except django.db.utils.IntegrityError:
                pass
            user.save()
            serializer = ClinicProfileSerializer(user.clinic_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif is_doctor is not None:
            user.is_doctor = is_doctor
            try:
                doctor = Doctor.objects.create(user=user)
                doctor.save()
            except django.db.utils.IntegrityError:
                pass
            user.save()
            serializer = DoctorProfileSerializer(user.doctor_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


