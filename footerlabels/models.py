from django.db import models


def upload_path_clinic_office(instance, filename):
    return '/'.join(['images/clinic_offices', str(instance.id), str(instance.name), filename])


def upload_path_collaborator_doctor(instance, filename):
    return '/'.join(['images/collaborator_doctor', str(instance.id), str(instance.first_name), str(instance.last_name), filename])


def upload_path_banner_image(instance, filename):
    return '/'.join(['images/banner', str(instance.id), str(instance.title), filename])


def upload_path_addsense_image(instance, filename):
    return '/'.join(['images/add_sense', str(instance.id), str(instance.alt), filename])


def upload_path_facilities(instance, filename):
    return '/'.join(['images/facilities', str(instance.id), str(instance.label), filename])


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
        verbose_name = 'Grad Medical'
        verbose_name_plural = 'Grade Medicale'

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
    icon = models.ImageField(upload_to=upload_path_facilities, blank=True, null=True)

    class Meta:
        verbose_name = 'Facilitate Unitate'
        verbose_name_plural = 'Facilitati Unitate'

    def __str__(self):
        return self.label


def upload_path_doctor(instance, filename):
    return '/'.join(['images/doctor', str(instance.id), filename])


class Newsletter(models.Model):
    name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(blank=False)

    class Meta:
        verbose_name = 'Newsletter Email'
        verbose_name_plural = 'Newsletter Emails'

    def __str__(self):
        return f'Nume: {self.name}, Email: {self.email}'


class BannerCards(models.Model):
    title = models.CharField(max_length=255, blank=False)
    subtitle = models.CharField(max_length=255, blank=False)
    link = models.CharField(max_length=255, blank=False)
    profile_picture = models.ImageField(upload_to=upload_path_banner_image, blank=True, null=True)

    class Meta:
        verbose_name = 'Banner Card'
        verbose_name_plural = 'Banners Cards'

    def __str__(self):
        return f'Titlu: {self.title}, id: {self.id}'


class AddSense(models.Model):
    href = models.CharField(max_length=500, blank=False)
    alt = models.CharField(max_length=255, blank=False)
    location = models.CharField(max_length=255, blank=False)
    photo = models.ImageField(upload_to=upload_path_addsense_image, blank=False)
    size = models.CharField(max_length=255, blank=False)

    class Meta:
        verbose_name = 'Add Sense'
        verbose_name_plural = 'Add-uri Sense'

    def __str__(self):
        return f'Titlu: {self.alt}, id: {self.id}'


def upload_path_blog_banner_image(instance, filename):
    return '/'.join(['images/blog', str(instance.id), str(instance.title), "banner", filename])


def upload_path_blog_image_1_image(instance, filename):
    return '/'.join(['images/blog', str(instance.id), str(instance.title), "img1", filename])


def upload_path_blog_image_2_image(instance, filename):
    return '/'.join(['images/blog', str(instance.id), str(instance.title), "img2", filename])


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tag Blog'
        verbose_name_plural = 'Taguri Blog'


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', related_name='blogposts', blank=True)
    banner_image = models.ImageField(upload_to=upload_path_blog_banner_image, blank=True, null=True)
    headline_1 = models.CharField(max_length=255)
    content_1 = models.TextField()
    image_1 = models.ImageField(upload_to=upload_path_blog_image_1_image, blank=True, null=True)
    headline_2 = models.CharField(max_length=255)
    content_2 = models.TextField()
    image_2 = models.ImageField(upload_to=upload_path_blog_image_2_image, blank=True, null=True)

    def __str__(self):
        return str(self.id) + " " + self.title

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blog'

