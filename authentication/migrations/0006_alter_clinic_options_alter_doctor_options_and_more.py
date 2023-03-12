# Generated by Django 4.1.4 on 2023-03-03 12:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('footerlabels', '0004_collaboratordoctor_clinicoffice'),
        ('authentication', '0005_user_is_visible'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clinic',
            options={'verbose_name': 'Clinica', 'verbose_name_plural': 'Clinici'},
        ),
        migrations.AlterModelOptions(
            name='doctor',
            options={'verbose_name': 'Doctor', 'verbose_name_plural': 'Doctori'},
        ),
        migrations.AlterModelOptions(
            name='document',
            options={'verbose_name': 'Document', 'verbose_name_plural': 'Documente'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Utilizator', 'verbose_name_plural': 'Utilizatori'},
        ),
        migrations.AddField(
            model_name='clinic',
            name='clinic_county',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='clinic',
            name='clinic_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='clinic',
            name='clinic_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='clinic',
            name='clinic_offices',
            field=models.ManyToManyField(to='footerlabels.clinicoffice'),
        ),
        migrations.AddField(
            model_name='clinic',
            name='clinic_other_details',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='clinic',
            name='clinic_schedule',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='clinic',
            name='clinic_specialities',
            field=models.ManyToManyField(to='footerlabels.clinicspecialities'),
        ),
        migrations.AddField(
            model_name='clinic',
            name='clinic_street',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='clinic',
            name='clinic_town',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='clinic',
            name='collaborator_doctor',
            field=models.ManyToManyField(to='footerlabels.collaboratordoctor'),
        ),
        migrations.AddField(
            model_name='clinic',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='clinic',
            name='primary_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='clinic',
            name='primary_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None),
        ),
        migrations.AddField(
            model_name='clinic',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='images/clinic/'),
        ),
        migrations.AddField(
            model_name='clinic',
            name='secondary_email',
            field=models.CharField(blank=True, max_length=610, null=True),
        ),
        migrations.AddField(
            model_name='clinic',
            name='secondary_phone',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='clinic',
            name='unity_facilities',
            field=models.ManyToManyField(to='footerlabels.medicalfacilities'),
        ),
        migrations.AddField(
            model_name='clinic',
            name='website',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='clinic',
            name='website_facebook',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='clinic',
            name='website_google',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='clinic',
            name='website_linkedin',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='clinic',
            name='website_youtube',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='images/users/'),
        ),
        migrations.AlterField(
            model_name='clinic',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clinic_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]