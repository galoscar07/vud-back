# Generated by Django 4.1.4 on 2023-03-07 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('footerlabels', '0005_alter_clinicoffice_profile_picture_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]