from django.db import models


class Footerlabels(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    label = models.CharField(max_length=100, blank=False)
    link = models.CharField(max_length=100, blank=False)

    class Meta:
        ordering = ['created']
        verbose_name = 'Eticheta Footer'
        verbose_name_plural = 'Etichete Footer'

    def __str__(self):
        return self.label + ' link:' + self.link


class MedicalUnityTypes(models.Model):
    label = models.CharField(max_length=60)

    class Meta:
        verbose_name = 'Tip Unitate Medicala'
        verbose_name_plural = 'Tipuri Unitate Medicala'

    def __str__(self):
        return self.label


class AcademicDegree(models.Model):
    label = models.CharField(max_length=60)

    class Meta:
        verbose_name = 'Grad Academic'
        verbose_name_plural = 'Grade Academice'

    def __str__(self):
        return self.label


class Speciality(models.Model):
    label = models.CharField(max_length=60)

    class Meta:
        verbose_name = 'Specialitate'
        verbose_name_plural = 'Specialitati'

    def __str__(self):
        return self.label


class MedicalSkills(models.Model):
    label = models.CharField(max_length=60)

    class Meta:
        verbose_name = 'Competenta'
        verbose_name_plural = 'Competente'

    def __str__(self):
        return self.label


class ClinicSpecialities(models.Model):
    label = models.CharField(max_length=60)

    class Meta:
        verbose_name = 'Specialitate Unitate'
        verbose_name_plural = 'Specialitati Unitate'

    def __str__(self):
        return self.label


class MedicalFacilities(models.Model):
    label = models.CharField(max_length=60)

    class Meta:
        verbose_name = 'Facilitate Unitate'
        verbose_name_plural = 'Facilitati Unitate'

    def __str__(self):
        return self.label


def upload_path_clinic_office(instance, filename):
    return '/'.join(['images/clinic_offices', str(instance.id), str(instance.name), filename])


def upload_path_collaborator_doctor(instance, filename):
    return '/'.join(['images/collaborator_doctor', str(instance.id), str(instance.doctor_name), filename])


class ClinicOffice(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to=upload_path_clinic_office, blank=True, null=True)
    medical_unit_types = models.ManyToManyField(MedicalUnityTypes)


class CollaboratorDoctor(models.Model):
    profile_picture = models.ImageField(upload_to=upload_path_collaborator_doctor, blank=True, null=True)
    doctor_name = models.CharField(max_length=255, blank=True, null=True)
    academic_degree = models.ManyToManyField(AcademicDegree)
    speciality = models.ManyToManyField(Speciality)
    medical_skill = models.ManyToManyField(MedicalSkills)
    link = models.CharField(max_length=255, blank=True, null=True)
