# Generated by Django 4.1.4 on 2023-03-18 21:42

from django.db import migrations, models
import footerlabels.models


class Migration(migrations.Migration):

    dependencies = [
        ('footerlabels', '0007_bannercards_alter_clinicoffice_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalfacilities',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to=footerlabels.models.upload_path_facilities),
        ),
    ]
