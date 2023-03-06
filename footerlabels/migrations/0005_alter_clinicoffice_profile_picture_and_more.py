# Generated by Django 4.1.4 on 2023-03-06 10:13

from django.db import migrations, models
import footerlabels.models


class Migration(migrations.Migration):

    dependencies = [
        ('footerlabels', '0004_collaboratordoctor_clinicoffice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinicoffice',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to=footerlabels.models.upload_path_clinic_office),
        ),
        migrations.AlterField(
            model_name='collaboratordoctor',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to=footerlabels.models.upload_path_collaborator_doctor),
        ),
    ]
