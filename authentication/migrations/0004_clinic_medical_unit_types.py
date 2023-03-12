# Generated by Django 4.1.4 on 2023-03-01 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('footerlabels', '0002_medicalunitytypes'),
        ('authentication', '0003_clinic_company_role_clinic_county_clinic_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='clinic',
            name='medical_unit_types',
            field=models.ManyToManyField(to='footerlabels.medicalunitytypes'),
        ),
    ]