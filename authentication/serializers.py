from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from authentication.models import User, Doctor, Clinic, ClinicReview
from footerlabels.serializers import ClinicSpecialitiesSerializer, MedicalFacilitiesSerializer, \
    MedicalUnityTypesSerializer, CollaboratorDoctorSerializer


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', None)
        if not email:
            raise serializers.ValidationError('Email should not be empty')
        return attrs
        # return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    refresh_token = serializers.CharField(max_length=555, read_only=True)
    access_token = serializers.CharField(max_length=555, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'profile_picture', 'last_name', 'first_name', 'refresh_token', 'access_token']

    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')

        if not user.is_active:
            raise AuthenticationFailed('Account not active yet')

        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        tokens = user.tokens()

        return {
            'email': user.email,
            'refresh_token': tokens['refresh'],
            'access_token': tokens['access'],
            'profile_photo': user.profile_picture,
            'first_name': user.first_name,
            'last_name': user.last_name
        }


class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']


class PasswordTokenCheckSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb = attrs.get('uidb')
            user = User.objects.get(id=force_str(urlsafe_base64_decode(uidb)))
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()
            return user
        except User.DoesNotExist:
            pass
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)


class DeleteUserSerializer(serializers.Serializer):
    confirm_password = serializers.CharField(max_length=128)


class UserUpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_clinic', 'is_doctor']


class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicReview
        fields = '__all__'


class ClinicProfileSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    clinic_specialities = ClinicSpecialitiesSerializer(many=True, read_only=True)
    unity_facilities = MedicalFacilitiesSerializer(many=True, read_only=True)
    medical_unit_types = MedicalUnityTypesSerializer(many=True, read_only=True)
    collaborator_doctor = CollaboratorDoctorSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)

    def get_reviews(self, obj):
        visible_reviews = obj.reviews.filter(is_visible=True)
        serializer = ReviewSerializer(visible_reviews, many=True)
        return serializer.data

    class Meta:
        model = Clinic
        fields = '__all__'


class ClinicProfileSimpleSerializer(serializers.ModelSerializer):
    clinic_specialities = ClinicSpecialitiesSerializer(many=True, read_only=True)
    unity_facilities = MedicalFacilitiesSerializer(many=True, read_only=True)
    medical_unit_types = MedicalUnityTypesSerializer(many=True, read_only=True)
    collaborator_doctor = CollaboratorDoctorSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Clinic
        fields = '__all__'
