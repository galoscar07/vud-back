from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.utils import Util
from footerlabels.models import MedicalUnityTypes, ClinicSpecialities, MedicalFacilities, \
    MedicalSkills, Speciality, AcademicDegree


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
    company = models.CharField(max_length=255)
    company_role = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    county = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=255)

    # Step will be the step in the auth in which the user is
    step = models.CharField(max_length=2, default=0, blank=False)

    # Clinics Data
    profile_picture = models.ImageField(upload_to=upload_path_clinic, blank=True, null=True)
    clinic_name = models.CharField(max_length=255)
    clinic_street = models.CharField(max_length=255)
    clinic_number = models.CharField(max_length=255)
    clinic_town = models.CharField(max_length=255)
    clinic_county = models.CharField(max_length=255)
    clinic_other_details = models.CharField(max_length=255, blank=True, null=True)
    primary_phone = models.CharField(max_length=255)
    secondary_phone = models.CharField(max_length=255, blank=True, null=True)
    primary_email = models.EmailField()
    secondary_email = models.CharField(max_length=610, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    website_facebook = models.CharField(max_length=255, blank=True, null=True)
    website_google = models.CharField(max_length=255, blank=True, null=True)
    website_linkedin = models.CharField(max_length=255, blank=True, null=True)
    website_youtube = models.CharField(max_length=255, blank=True, null=True)
    whatsapp = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(max_length=500)

    # Collab
    collaborator_doctor = models.ManyToManyField('CollaboratorDoctor', blank=True)
    collaborator_clinic = models.ManyToManyField('self', blank=True)

    # Clinic Speciality
    clinic_specialities = models.ManyToManyField(ClinicSpecialities)

    # Unity Facilities
    unity_facilities = models.ManyToManyField(MedicalFacilities)

    # Medical Unity Types
    medical_unit_types = models.ManyToManyField(MedicalUnityTypes)

    # Schedule
    clinic_schedule = models.TextField()

    # Is visible
    is_visible = models.BooleanField(default=False)
    is_notification_email_send = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Clinica'
        verbose_name_plural = 'Clinici'

    def __str__(self):
        return f'Nume clinica: {self.clinic_name}, firma: {self.company} - {self.clinic_town}'

    def save(self, *args, **kwargs):
        if self.is_visible and not self.is_notification_email_send:
            data = {'email': self.user.email}
            Util.send_email(data=data, email_type='account-approved')
            self.is_notification_email_send = True
        super().save(*args, **kwargs)


def upload_path_collaborator_doctor(instance, filename):
    return '/'.join(['images/collaborator_doctor', str(instance.id), str(instance.first_name), str(instance.last_name), filename])


class CollaboratorDoctor(models.Model):
    user = models.OneToOneField(User, related_name='doctor_profile', on_delete=models.CASCADE, blank=True, null=True)

    profile_picture = models.ImageField(upload_to=upload_path_collaborator_doctor, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    primary_phone = models.CharField(max_length=255)
    phone_vud = models.CharField(max_length=255)
    primary_email = models.EmailField()
    website = models.CharField(max_length=255, blank=True, null=True)
    website_facebook = models.CharField(max_length=255, blank=True, null=True)
    website_google = models.CharField(max_length=255, blank=True, null=True)
    website_linkedin = models.CharField(max_length=255, blank=True, null=True)
    website_youtube = models.CharField(max_length=255, blank=True, null=True)
    whatsapp = models.CharField(max_length=255, blank=True, null=True)

    # Description
    description = models.TextField(max_length=500)

    # Specialities
    academic_degree = models.ManyToManyField(AcademicDegree)
    speciality = models.ManyToManyField(Speciality)
    medical_skill = models.ManyToManyField(MedicalSkills)

    # Collab
    collaborator_doctor = models.ManyToManyField('self', symmetrical=False, blank=True)
    collaborator_clinic = models.ManyToManyField(Clinic, blank=True)

    # Step
    step = models.CharField(max_length=2, default=0, blank=False)

    # Is visible
    is_visible = models.BooleanField(default=False)
    is_notification_email_send = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctori'

    def __str__(self):
        try:
            spec = self.speciality.all()[0].label
        except Exception:
            spec = 'Nu este selectata specialitate'
        return f'{self.first_name} {self.last_name} - {spec}'

    def save(self, *args, **kwargs):
        if self.is_visible and not self.is_notification_email_send:
            data = {'email': self.user.email}
            Util.send_email(data=data, email_type='account-approved')
            self.is_notification_email_send = True
        super().save(*args, **kwargs)


# @receiver(models.signals.post_save, sender=CollaboratorDoctor)
# def send_email_on_visibility_change_doctor(sender, instance, **kwargs):
#     if instance.is_visible and kwargs.get('created', False) and instance.user:
#         data = {'email': instance.user.email}
#         Util.send_email(data=data, email_type='account-approved')


class DoctorReview(models.Model):
    doctor = models.ForeignKey(CollaboratorDoctor, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=False)

    def __str__(self):
        return f'{"Aprobat" if self.is_visible else "Neaprobat"}, Doctor {self.doctor.first_name} {self.doctor.last_name}, Nume: {self.name}, Comentariu: {self.comment}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Review Doctor'
        verbose_name_plural = 'Reviews Doctori'


class ClinicReview(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=False)

    def __str__(self):
        return f'{"Aprobat" if self.is_visible else "Neaprobat"}, Clinica {self.clinic.clinic_name}, Nume: {self.name}, Comentariu: {self.comment}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Review Clinica'
        verbose_name_plural = 'Reviews Clinici'


def upload_path_clinic_office(instance, filename):
    return '/'.join(['files/documents', str(instance.id), filename])


class Document(models.Model):
    owner = models.ForeignKey('User', related_name="files",  on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_path_clinic_office)

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documente'

    def __str__(self):
        return f'{self.owner.first_name} {self.owner.last_name} - {self.owner.email} - {self.id}'


class RequestToRedeemClinic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clinic_to_redeem = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    company_role = models.CharField(max_length=50)
    message = models.TextField()
    ACCEPTED_CHOICES = (
        ('default', 'Neselectat'),
        ('acceptat', 'Acceptat'),
        ('respins', 'Respins'),
    )
    accepted = models.CharField(max_length=10, choices=ACCEPTED_CHOICES, default='default')

    def __str__(self):
        return f"Status: {self.accepted}, {self.user.first_name} {self.user.last_name} - {self.company_role}"

    def save(self, *args, **kwargs):
        if self.accepted == 'acceptat':
            try:
                clinic = Clinic.objects.get(id=self.clinic_to_redeem)
            except Exception:
                clinic = None

            if clinic:
                clinic.user = self.user
                clinic.save()

                data = {'email': self.user.email}
                Util.send_email(data=data, email_type='account-approved')

        elif self.accepted == 'respins':
            data = {'email': self.user.email, 'name': self.user.first_name + ' ' + self.user.last_name}
            Util.send_email(data=data, email_type='account-denied')

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Revendicare Clinica'
        verbose_name_plural = 'Revendicari Clinici'


class RequestToRedeemDoctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doctor_to_redeem = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    message = models.TextField()
    ACCEPTED_CHOICES = (
        ('default', 'Neselectat'),
        ('acceptat', 'Acceptat'),
        ('respins', 'Respins'),
    )
    accepted = models.CharField(max_length=10, choices=ACCEPTED_CHOICES, default='default')

    def save(self, *args, **kwargs):
        if self.accepted == 'acceptat':
            try:
                doctor = CollaboratorDoctor.objects.get(id=self.doctor_to_redeem)
            except Exception:
                doctor = None

            if doctor:
                doctor.user = self.user
                doctor.save()

                data = {'email': self.user.email}
                Util.send_email(data=data, email_type='account-approved')

        elif self.accepted == 'respins':
            data = {'email': self.user.email, 'name': self.user.first_name + ' ' + self.user.last_name}
            Util.send_email(data=data, email_type='account-denied')

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Status: {self.accepted}, {self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = 'Revendicare Doctor'
        verbose_name_plural = 'Revendicari Doctori'

