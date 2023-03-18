from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken

from footerlabels.models import MedicalUnityTypes, ClinicOffice, ClinicSpecialities, MedicalFacilities, \
    CollaboratorDoctor


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
    # Email of the user
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    # Used for verifying email address
    is_verified = models.BooleanField(default=False)
    # Used for making the account visible
    is_visible = models.BooleanField(default=False, )
    # Only for admin user
    is_staff = models.BooleanField(default=False)

    # Used for python django, leave like that
    is_active = models.BooleanField(default=True)
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

    # Profile Picture
    profile_picture = models.ImageField(upload_to='images/users/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = 'Utilizator'
        verbose_name_plural = 'Utilizatori'

    def __str__(self):
        if self.is_doctor:
            return f'email: {self.email}, rol: doctor, id: {self.id}'
        if self.is_clinic:
            return f'email: {self.email}, rol: clinica, id: {self.id}'
        if self.is_staff:
            return f'email: {self.email}, rol: staff, id: {self.id}'
        return f'Role: {"doctor" if self.is_doctor else "clinic" if self.is_clinic else "none"}, Email: {self.email}, id: {self.id}'

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


def upload_path_clinic(instance, filename):
    return '/'.join(['images/clinic', str(instance.id), filename])


class Clinic(models.Model):
    user = models.OneToOneField(User, related_name='clinic_profile', on_delete=models.CASCADE, blank=True, null=True)

    # Admin Data
    role = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    company_role = models.CharField(max_length=255, blank=True)
    town = models.CharField(max_length=255, blank=True)
    county = models.CharField(max_length=255, blank=True)
    street = models.CharField(max_length=255, blank=True)
    number = models.CharField(max_length=255, blank=True)

    # Step will be the step in the auth in which the user is
    step = models.CharField(max_length=2, default=0, blank=False)

    # Clinics Data
    profile_picture = models.ImageField(upload_to=upload_path_clinic, blank=True, null=True)
    clinic_name = models.CharField(max_length=255, blank=True, null=True)
    clinic_street = models.CharField(max_length=255, blank=True, null=True)
    clinic_number = models.CharField(max_length=255, blank=True, null=True)
    clinic_town = models.CharField(max_length=255, blank=True, null=True)
    clinic_county = models.CharField(max_length=255, blank=True, null=True)
    clinic_other_details = models.CharField(max_length=255, blank=True, null=True)
    primary_phone = PhoneNumberField(blank=True)
    secondary_phone = models.CharField(max_length=255, blank=True, null=True)
    primary_email = models.EmailField(blank=True)
    secondary_email = models.CharField(max_length=610, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    website_facebook = models.CharField(max_length=255, blank=True, null=True)
    website_google = models.CharField(max_length=255, blank=True, null=True)
    website_linkedin = models.CharField(max_length=255, blank=True, null=True)
    website_youtube = models.CharField(max_length=255, blank=True, null=True)
    whatsapp = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    # Doctor Collaborator
    collaborator_doctor = models.ManyToManyField(CollaboratorDoctor)

    # Clinic offices
    clinic_offices = models.ManyToManyField(ClinicOffice)

    # Clinic Speciality
    clinic_specialities = models.ManyToManyField(ClinicSpecialities)

    # Unity Facilities
    unity_facilities = models.ManyToManyField(MedicalFacilities)

    # Medical Unity Types
    medical_unit_types = models.ManyToManyField(MedicalUnityTypes)

    # Schedule
    clinic_schedule = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Clinica'
        verbose_name_plural = 'Clinici'

    def __str__(self):
        return f'Id utilizator: {self.user.id}, companie: {self.company}, clinic_id: {self.id}'


class ClinicReview(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=False)

    def __str__(self):
        return f'Is_visible:{self.is_visible}, Clinic Name {self.clinic.clinic_name}, Name: {self.name}, Comment: {self.comment}'

    class Meta:
        ordering = ['-created_at']


class Doctor(models.Model):
    user = models.OneToOneField(User, related_name='doctor_profile', on_delete=models.CASCADE)
    # TODO add the rest of the fields

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctori'

    def __str__(self):
        return f'Id utilizator: {self.user.id}, nume: {self.user.first_name} {self.user.last_name}'


class Document(models.Model):
    owner = models.ForeignKey('User', related_name="files",  on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    file = models.FileField()

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documente'

    def __str__(self):
        return f'Document: {self.name}, detinator: {self.owner.id}'




