import django.db
import jwt
import json

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
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

from footerlabels.models import MedicalUnityTypes, ClinicSpecialities, MedicalFacilities
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


class RequestPasswordResetAPIView(APIView):
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
            absolute_url = f'https://vud-fe.herokuapp.com/reset-password/?token={str(token)}&uidb={str(uidb64)}'
            # relative_link = reverse('password-reset-confirm', kwargs={'uidb': uidb64, 'token': token})
            # absolute_url = f'http://{current_site}{relative_link}'
            data = {
                'url': absolute_url,
                'email': user.email
            }
            Util.send_email(data=data, email_type='verify-email')
            print(absolute_url)

            return Response({'url': absolute_url}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_200_OK)


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
                clinic_profile = user.clinic_profile
                if clinic_profile.step != '5':
                    return Response({"step": clinic_profile.step}, status=200)
                if not user.is_visible:
                    return Response({"step": 5}, status=200)
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
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        is_clinic = request.data.get('is_clinic', None)
        is_doctor = request.data.get('is_doctor', None)

        if is_clinic is not None:
            user.is_clinic = is_clinic
            try:
                clinic = Clinic.objects.create(user=user)
                clinic.step = 2
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


class UpdateAdminData(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                'contact_email': openapi.Schema(type=openapi.TYPE_STRING),
                'phone_number_optional': openapi.Schema(type=openapi.TYPE_STRING),
                'contact_email_optional': openapi.Schema(type=openapi.TYPE_STRING),
                'company': openapi.Schema(type=openapi.TYPE_STRING),
                'company_role': openapi.Schema(type=openapi.TYPE_STRING),
                'county': openapi.Schema(type=openapi.TYPE_STRING),
                'town': openapi.Schema(type=openapi.TYPE_STRING),
                'street': openapi.Schema(type=openapi.TYPE_STRING),
                'number': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )
    def put(self, request):
        user = request.user

        if user.is_authenticated:

            # Save user data
            user.first_name = request.data.get('first_name', '')
            user.last_name = request.data.get('last_name', '')
            user.phone_number = request.data.get('phone_number', '')
            user.contact_email = request.data.get('contact_email', '')
            user.phone_number_optional = request.data.get('phone_number_optional', '')
            user.contact_email_optional = request.data.get('contact_email_optional', '')
            # Save clinic data
            try:
                clinic_profile = Clinic.objects.get(user=user)
                clinic_profile.company = request.data.get('company', '')
                clinic_profile.company_role = request.data.get('company_role', '')
                clinic_profile.town = request.data.get('town', '')
                clinic_profile.county = request.data.get('county', '')
                clinic_profile.street = request.data.get('street', '')
                clinic_profile.number = request.data.get('number', '')
                clinic_profile.step = 3
                clinic_profile.save()
            except Clinic.DoesNotExist as e:
                return Response({'error': 'Clinic profile does\'t exist'})

            # Save the data
            user.save()

        return Response({'success': 'Saved'}, status=200)


class UpdateClinicTypeData(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'list_of_clinic_types': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                       description='Expected a list of ids representing the id of a '
                                                                   'clinic type',
                                                       items=openapi.Schema(type=openapi.TYPE_STRING)),
            }
        )
    )
    def put(self, request):
        user = request.user
        if user.is_authenticated:
            try:
                list_of_clinic_types = request.data.get('list_of_clinic_types')
                clinic_profile = user.clinic_profile
                for elem in list_of_clinic_types:
                    clinic_type = MedicalUnityTypes.objects.get(id=elem)
                    clinic_profile.medical_unit_types.add(clinic_type)
                clinic_profile.step = 4
                clinic_profile.save()
                return Response({"success": 'Success'}, status=200)
            except Exception as s:
                return Response({"error": s}, status=400)


class UpdateClinicProfileView(APIView):
    def put(self, request):
        user = request.user
        # check user is authenticated + user have clinic progfile
        if not user.is_authenticated:
            return Response({"error": 'Not logged'}, status=401)
        if not user.is_clinic or not user.clinic_profile:
            return Response({"error": 'No clinic profile'}, status=400)
        # after you checked get the data from request
        clinic_name = request.data.get('clinic_name', None)
        clinic_street = request.data.get('clinic_street', None)
        clinic_number = request.data.get('clinic_number', None)
        clinic_town = request.data.get('clinic_town', None)
        clinic_county = request.data.get('clinic_county', None)
        clinic_other_details = request.data.get('clinic_other_details', None)
        primary_phone = request.data.get('primary_phone', None)
        secondary_phone = request.data.get('secondary_phone', None)
        primary_email = request.data.get('primary_email', None)
        secondary_email = request.data.get('secondary_email', None)
        website = request.data.get('website', None)
        website_facebook = request.data.get('website_facebook', None)
        website_google = request.data.get('website_google', None)
        website_linkedin = request.data.get('website_linkedin', None)
        website_youtube = request.data.get('website_youtube', None)
        description = request.data.get('description', None)
        clinic_specialities = request.data.get('clinic_specialities', None)
        clinic_schedule = request.data.get('clinic_schedule', None)

        if clinic_specialities:
            clinic_specialities = json.loads(clinic_specialities)
        clinic_facilities = request.data.get('clinic_facilities', None)
        if clinic_facilities:
            clinic_facilities = json.loads(clinic_facilities)
        hq = request.data.get('hq', None)
        if hq:
            hq = json.loads(hq)
        doctors = request.data.get('doctor', None)
        if doctors:
            doctors = json.loads(doctors)

        clinic_profile = user.clinic_profile
        clinic_profile.clinic_name = clinic_name
        clinic_profile.clinic_street = clinic_street
        clinic_profile.clinic_number = clinic_number
        clinic_profile.clinic_town = clinic_town
        clinic_profile.clinic_county = clinic_county
        clinic_profile.clinic_other_details = clinic_other_details
        clinic_profile.primary_phone = primary_phone
        clinic_profile.secondary_phone = secondary_phone
        clinic_profile.primary_email = primary_email
        clinic_profile.secondary_email = secondary_email
        clinic_profile.website = website
        clinic_profile.website_facebook = website_facebook
        clinic_profile.website_google = website_google
        clinic_profile.website_linkedin = website_linkedin
        clinic_profile.website_youtube = website_youtube
        clinic_profile.description = description
        clinic_profile.clinic_schedule = clinic_schedule
        clinic_profile.step = 5

        for cs in clinic_specialities:
            try:
                clinic_spec = ClinicSpecialities.objects.get(id=cs)
                clinic_profile.clinic_specialities.add(clinic_spec)
            except ClinicSpecialities.DoesNotExist:
                pass

        for cf in clinic_facilities:
            try:
                clinic_fac = MedicalFacilities.objects.get(id=cf)
                clinic_profile.unity_facilities.add(clinic_fac)
            except MedicalFacilities.DoesNotExist:
                pass

        # TODO implement this
        # photoKeys = request.data.get('photoKeys', None)
        # if photoKeys:
        #     import pdb;pdb.set_trace()

        clinic_profile.save()
        return Response({"success": "Success"}, status=200)
