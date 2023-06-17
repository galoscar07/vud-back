import string
from random import choices

import django.db
import jwt
import json

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from rest_framework import generics, status, views, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer, \
    ResetPasswordEmailSerializer, SetNewPasswordSerializer, PasswordTokenCheckSerializer, \
    UserUpdateUserProfileSerializer, ClinicProfileSerializer, DoctorProfileSerializer, DeleteUserSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from footerlabels.models import MedicalUnityTypes, ClinicSpecialities, MedicalFacilities, AcademicDegree, Speciality
from .models import User, Clinic, Document, RequestToRedeemClinic, CollaboratorDoctor, RequestToRedeemDoctor
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

        absolute_url = f'https://vreaudoctor.ro/email-verification/{str(token)}/'

        data = {
            'url': absolute_url,
            'email': user.email
        }
        Util.send_email(data=data, email_type='verify-email')

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

            absolute_url = f'https://vreaudoctor.ro/email-verification/{str(token)}/'

            data = {
                'url': absolute_url,
                'email': user.email
            }
            Util.send_email(data=data, email_type='verify-email')

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
            absolute_url = f'https://vreaudoctor.ro/email-verification/?token={str(token)}&uidb={str(uidb64)}'

            data = {
                'url': absolute_url,
                'email': user.email
            }
            Util.send_email(data=data, email_type='reset-password')

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


class DeleteUserView(generics.DestroyAPIView):
    serializer_class = DeleteUserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        password = serializer.validated_data['confirm_password']
        if not user.check_password(password):
            return Response({'confirm_password': 'Invalid password'},
                            status=status.HTTP_400_BAD_REQUEST)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        is_clinic = request.data.get('is_clinic', None)
        is_doctor = request.data.get('is_doctor', None)

        if is_clinic:
            user.is_clinic = is_clinic
            try:
                clinic = Clinic.objects.create(user=user)
                clinic.step = 2
                clinic.save()
            except django.db.utils.IntegrityError:
                pass
            user.save()
            serializer = ClinicProfileSerializer(user.clinic_profile)
            data_to_be_send = serializer.data
            data_to_be_send['is_clinic'] = True
            return Response(data_to_be_send, status=status.HTTP_200_OK)

        elif is_doctor:
            user.is_doctor = is_doctor
            try:
                doctor = CollaboratorDoctor.objects.create(user=user)
                doctor.step = 2
                doctor.save()
            except django.db.utils.IntegrityError:
                pass
            user.save()
            serializer = DoctorProfileSerializer(user.doctor_profile)
            data_to_be_send = serializer.data
            data_to_be_send['is_doctor'] = True
            return Response(data_to_be_send, status=status.HTTP_200_OK)

        return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateAdminData(APIView):
    permission_classes = (permissions.IsAuthenticated,)

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
            # TODO Check file saving
            file1 = request.data.get('file1', None)
            file2 = request.data.get('file2', None)
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
                doc1 = Document.objects.create(owner=user, file=file1)
                doc2 = Document.objects.create(owner=user, file=file2)
                doc1.save()
                doc2.save()
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
        whatsapp = request.data.get('whatsapp', None)
        description = request.data.get('description', None)
        clinic_schedule = request.data.get('clinic_schedule', None)
        profile_picture = request.data.get('profile_picture', None)

        clinic_specialities = request.data.get('clinic_specialities', None)
        if clinic_specialities:
            clinic_specialities = json.loads(clinic_specialities)

        clinic_facilities = request.data.get('clinic_facilities', None)
        if clinic_facilities:
            clinic_facilities = json.loads(clinic_facilities)

        doctors = request.data.get('doctor', "").split("|")
        clinics = request.data.get('clinic', "").split("|")

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
        clinic_profile.whatsapp = whatsapp
        clinic_profile.description = description
        clinic_profile.clinic_schedule = clinic_schedule
        clinic_profile.profile_picture = profile_picture
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

        if len(doctors) > 200:
            return Response({"error": "Nu poti adaug mai mult de 200 de doctori"}, status=400)

        if len(clinics) > 200:
            return Response({"error": "Nu poti adaug mai mult de 200 de clinici"}, status=400)

        for doc in doctors:
            try:
                doctor = CollaboratorDoctor.objects.get(id=doc)
                clinic_profile.collaborator_doctor.add(doctor)
            except Exception:
                pass

        for clinic in clinics:
            try:
                clin = Clinic.objects.get(id=clinic)
                clinic_profile.collaborator_doctor.add(clin)
            except Exception:
                pass

        # Send email thanks sing up
        data = {
            'email': user.email
        }
        Util.send_email(data=data, email_type='thank-you-sign-up')

        clinic_profile.save()
        return Response({"success": "Success"}, status=200)


class UpdateDoctorProfileView(APIView):
    def put(self, request):
        user = request.user
        # check user is authenticated + user have clinic progfile
        if not user.is_authenticated:
            return Response({"error": 'Not logged'}, status=401)
        if not user.is_doctor or not user.doctor_profile:
            return Response({"error": 'No clinic profile'}, status=400)
        # after you checked get the data from request
        first_name = request.data.get('first_name', None)
        last_name = request.data.get('last_name', None)
        primary_phone = request.data.get('primary_phone', None)
        primary_phone_vud = request.data.get('primary_phone_vud', None)
        primary_email = request.data.get('primary_email', None)
        website = request.data.get('website', None)
        website_facebook = request.data.get('website_facebook', None)
        website_google = request.data.get('website_google', None)
        website_linkedin = request.data.get('website_linkedin', None)
        website_youtube = request.data.get('website_youtube', None)
        whatsapp = request.data.get('whatsapp', None)
        description = request.data.get('description', None)

        doctors = request.data.get('doctor', "").split("|")
        clinics = request.data.get('clinic', "").split("|")

        academic_degree = request.data.get('academic_degree', None)
        if academic_degree:
            academic_degree = json.loads(academic_degree)

        speciality = request.data.get('speciality', None)
        if speciality:
            speciality = json.loads(speciality)

        medical_skill = request.data.get('medical_skill', None)
        if medical_skill:
            medical_skill = json.loads(medical_skill)

        doctor_profile = user.doctor_profile

        doctor_profile.first_name = first_name
        doctor_profile.last_name = last_name
        doctor_profile.primary_phone = primary_phone
        doctor_profile.phone_vud = primary_phone_vud
        doctor_profile.primary_email = primary_email
        doctor_profile.website = website
        doctor_profile.website_facebook = website_facebook
        doctor_profile.website_google = website_google
        doctor_profile.website_linkedin = website_linkedin
        doctor_profile.website_youtube = website_youtube
        doctor_profile.whatsapp = whatsapp
        doctor_profile.description = description
        doctor_profile.step = 5

        for ad in academic_degree:
            try:
                doc_ad = AcademicDegree.objects.get(id=ad)
                doctor_profile.academic_degree.add(doc_ad)
            except AcademicDegree.DoesNotExist:
                pass

        for spec in speciality:
            try:
                doc_spec = Speciality.objects.get(id=spec)
                doctor_profile.speciality.add(doc_spec)
            except Speciality.DoesNotExist:
                pass

        for ms in medical_skill:
            try:
                doc_ms = Speciality.objects.get(id=ms)
                doctor_profile.speciality.add(doc_ms)
            except Speciality.DoesNotExist:
                pass

        if len(doctors) > 200:
            return Response({"error": "Nu poti adaug mai mult de 200 de doctori"}, status=400)

        if len(clinics) > 200:
            return Response({"error": "Nu poti adaug mai mult de 200 de clinici"}, status=400)

        for doc in doctors:
            try:
                doctor = CollaboratorDoctor.objects.get(id=doc)
                doctor_profile.collaborator_doctor.add(doctor)
                data = {
                    'email': doctor_profile.primary_email,
                    'to_name': doctor_profile.first_name,
                    'from_nane': doctor_profile.first_name + ' ' + doctor_profile.last_name,
                    'profile_link': 'www.vreaudoctor.ro/doctor-page/?id='+doctor_profile.id
                }
                Util.send_email(data=data, email_type='notification-invited-collab-doctor-to-clinic')
            except Exception:
                pass

        for clinic in clinics:
            try:
                clin = Clinic.objects.get(id=clinic)
                doctor_profile.collaborator_clinic.add(clin)
                data = {
                    'email': clin.primary_email,
                    'to_name': clin.clinic_name,
                    'from_nane': doctor_profile.first_name + ' ' + doctor_profile.last_name,
                    'profile_link': 'www.vreaudoctor.ro/doctor-page/?id='+doctor_profile.id
                }
                Util.send_email(data=data, email_type='notification-invited-collab-doctor-to-clinic')
            except Exception:
                pass

        file1 = request.data.get('file1', None)
        file2 = request.data.get('file2', None)

        doc1 = Document.objects.create(owner=user, file=file1)
        doc2 = Document.objects.create(owner=user, file=file2)
        doc1.save()
        doc2.save()

        doctor_profile.save()

        data = {
            'email': user.email
        }
        Util.send_email(data=data, email_type='thank-you-sign-up')

        return Response({"success": "Success"}, status=200)


@api_view(['POST'])
def invite_collaborator_doctor(request):
    user = request.user
    if not user:
        return Response({"error": "Error, user not logged"}, status=400)

    try:
        to_sent = request.data.get('name', '')
        email = request.data.get('email', '')
        message = request.data.get('message', None)
        from_sent = request.data.get('from_sent', '')
        from_type = request.data.get('from_type', '')
        type_added = 'medic colaborator'

        data = {
            'email': email,
            'custom': True if message else False,
            'message': message,
            'name': from_sent,
            'typeAdded': type_added,
            'type': from_type,
            'toSent': to_sent,
        }
        Util.send_email(data=data, email_type='invite-part-of-team')
        return Response({"success": "Success"}, status=200)

    except Exception:
        return Response({"error": "Error"}, status=400)


@api_view(['POST'])
def invite_collaborator_clinic(request):
    user = request.user
    if not user:
        return Response({"error": "Error, user not logged"}, status=400)

    try:
        to_sent = request.data.get('name', '')
        email = request.data.get('email', '')
        message = request.data.get('message', None)
        from_sent = request.data.get('from_sent', '')
        from_type = request.data.get('from_type', '')
        type_added = 'clinica colaboratoare'

        data = {
            'email': email,
            'custom': True if message else False,
            'message': message,
            'name': from_sent,
            'typeAdded': type_added,
            'type': from_type,
            'toSent': to_sent,
        }
        Util.send_email(data=data, email_type='invite-part-of-team')
        return Response({"success": "Success"}, status=200)

    except Exception:
        return Response({"error": "Error"}, status=400)


@api_view(['POST'])
def redeem_clinic_request(request):
    # Get parameters from request
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')
    email = request.data.get('email', '')
    phone = request.data.get('phone', '')
    company_role = request.data.get('company_role', '')
    message = request.data.get('message', '')
    clinic_id = request.data.get('clinic_id', '')
    file1 = request.data.get('file1', None)
    file2 = request.data.get('file2', None)

    # Generate random password
    password = ''.join(choices(string.ascii_letters + string.digits, k=12))

    # Create new user
    try:
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
        )
        user.save()
    except Exception:
        return Response({'error': True})

    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.save()

    # Create new request to sign up model
    RequestToRedeemClinic.objects.create(
        user=user,
        phone=phone,
        company_role=company_role,
        clinic_to_redeem=clinic_id,
        message=message,
    )

    if file1:
        Document.objects.create(owner=user, file=file1)
    if file2:
        Document.objects.create(owner=user, file=file2)

    return Response({'success': True})


@api_view(['POST'])
def redeem_doctor_request(request):
    # Get parameters from request
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')
    email = request.data.get('email', '')
    phone = request.data.get('phone', '')
    message = request.data.get('message', '')
    doctor = request.data.get('doctor_id', '')
    file1 = request.data.get('file1', None)
    file2 = request.data.get('file2', None)

    # Generate random password
    password = ''.join(choices(string.ascii_letters + string.digits, k=12))

    # Create new user
    try:
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
        )
    except Exception:
        return Response({'error': True})

    user.first_name = first_name
    user.last_name = last_name

    # Create new request to sign up model
    RequestToRedeemDoctor.objects.create(
        user=user,
        phone=phone,
        doctor_to_redeem=doctor,
        message=message,
    )

    if file1:
        Document.objects.create(owner=user, file=file1)
    if file2:
        Document.objects.create(owner=user, file=file2)

    return Response({'success': True})
