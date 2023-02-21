from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):

    def create_user(self, email, username=None, password=None):
        # if username is None:
        #     raise TypeError('Users should have a username')
        # import pdb;pdb.set_trace()
        # if email is None:
        #     raise TypeError('Users should have a email')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username=None, password=None):
        if password is None:
            raise TypeError('Password should not be none')
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    # TODO: Check if the below should be false and made true only by the admin when the profile is checked
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Fields for checking if a user is clinic or doctor
    is_clinic = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)

    # Fields for user
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    phone_number = PhoneNumberField(blank=True)
    contact_email = models.EmailField(blank=True)
    phone_number_optional = PhoneNumberField(blank=True)
    contact_email_optional = models.EmailField(blank=True)

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return f'Role: {"doctor" if self.is_doctor else "clinic" if self.is_clinic else "none"}, Email: {self.email}'

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class Clinic(models.Model):
    user = models.OneToOneField(User, related_name='clinic_profile', on_delete=models.CASCADE)
    role = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    # TODO add the rest of the fields


class Doctor(models.Model):
    user = models.OneToOneField(User, related_name='doctor_profile', on_delete=models.CASCADE)
    # TODO add the rest of the fields




